"""Tests for transparency MCP server — GovTrack, World Bank, ProPublica Nonprofit Explorer.

All HTTP calls are mocked. No network access required.
"""

import json
import sys
from pathlib import Path
from unittest.mock import AsyncMock, patch, MagicMock

import httpx
import pytest

# Add parent dir to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


# --- Fixtures ---

@pytest.fixture
def mock_response():
    """Factory for mock httpx.Response objects."""
    def _make(status_code=200, json_data=None, text=""):
        resp = MagicMock(spec=httpx.Response)
        resp.status_code = status_code
        resp.json.return_value = json_data or {}
        resp.text = text or json.dumps(json_data or {})
        resp.raise_for_status = MagicMock()
        if status_code >= 400:
            resp.raise_for_status.side_effect = httpx.HTTPStatusError(
                f"{status_code}", request=MagicMock(), response=resp
            )
        return resp
    return _make


# --- Module Structure Tests ---

class TestServerStructure:
    """Verify the MCP server is properly configured."""

    def test_importable(self):
        import transparency_server
        assert hasattr(transparency_server, "mcp")
        assert hasattr(transparency_server, "main_sync")

    def test_has_all_tools(self):
        """Server must expose all 8 tools."""
        import transparency_server
        expected = [
            "govtrack_members",
            "govtrack_bills",
            "govtrack_votes",
            "worldbank_indicator",
            "worldbank_search",
            "nonprofit_search",
            "nonprofit_details",
            "transparency_status",
        ]
        for name in expected:
            assert hasattr(transparency_server, name), f"Missing tool: {name}"


# --- GovTrack Tests ---

class TestGovTrackMembers:
    """Test govtrack_members tool."""

    @pytest.mark.asyncio
    async def test_returns_members(self, mock_response):
        """Returns formatted member list from GovTrack API."""
        api_data = {
            "objects": [
                {
                    "person": {
                        "firstname": "Nancy",
                        "lastname": "Pelosi",
                        "birthday": "1940-03-26",
                        "gender": "female",
                        "link": "https://www.govtrack.us/congress/members/nancy_pelosi/400314",
                    },
                    "role_type": "representative",
                    "state": "CA",
                    "district": 11,
                    "party": "Democrat",
                    "startdate": "2023-01-03",
                    "enddate": "2025-01-03",
                },
            ],
            "meta": {"total_count": 1},
        }
        resp = mock_response(json_data=api_data)

        with patch("transparency_server._govtrack_get", new_callable=AsyncMock, return_value=api_data):
            from transparency_server import govtrack_members
            result = await govtrack_members()
            assert "Pelosi" in result
            assert "CA" in result
            assert "Democrat" in result

    @pytest.mark.asyncio
    async def test_filters_by_state(self, mock_response):
        """Passes state filter to API."""
        api_data = {"objects": [], "meta": {"total_count": 0}}

        with patch("transparency_server._govtrack_get", new_callable=AsyncMock, return_value=api_data) as mock_get:
            from transparency_server import govtrack_members
            result = await govtrack_members(state="CA")
            mock_get.assert_called_once()
            call_args = mock_get.call_args
            assert call_args[0][0] == "role"
            assert call_args[1].get("params", {}).get("state") == "CA"

    @pytest.mark.asyncio
    async def test_api_error_handled(self):
        """Returns error message on API failure."""
        with patch("transparency_server._govtrack_get", new_callable=AsyncMock, side_effect=httpx.HTTPError("timeout")):
            from transparency_server import govtrack_members
            result = await govtrack_members()
            assert "error" in result.lower() or "Error" in result


class TestGovTrackBills:
    """Test govtrack_bills tool."""

    @pytest.mark.asyncio
    async def test_search_bills(self, mock_response):
        """Returns formatted bill search results."""
        api_data = {
            "objects": [
                {
                    "title": "Infrastructure Investment and Jobs Act",
                    "bill_type": "house_bill",
                    "number": 3684,
                    "congress": 117,
                    "current_status": "enacted_signed",
                    "introduced_date": "2021-06-04",
                    "link": "https://www.govtrack.us/congress/bills/117/hr3684",
                },
            ],
            "meta": {"total_count": 1},
        }

        with patch("transparency_server._govtrack_get", new_callable=AsyncMock, return_value=api_data):
            from transparency_server import govtrack_bills
            result = await govtrack_bills(query="infrastructure")
            assert "Infrastructure" in result
            assert "enacted" in result.lower() or "signed" in result.lower()

    @pytest.mark.asyncio
    async def test_empty_results(self):
        """Returns no results message for empty search."""
        api_data = {"objects": [], "meta": {"total_count": 0}}

        with patch("transparency_server._govtrack_get", new_callable=AsyncMock, return_value=api_data):
            from transparency_server import govtrack_bills
            result = await govtrack_bills(query="xyznonexistent")
            assert "no" in result.lower() or "0" in result


class TestGovTrackVotes:
    """Test govtrack_votes tool."""

    @pytest.mark.asyncio
    async def test_returns_votes(self, mock_response):
        """Returns formatted voting records."""
        api_data = {
            "objects": [
                {
                    "question": "On Passage of the Bill",
                    "created": "2023-06-01T12:00:00Z",
                    "category": "passage",
                    "result": "Passed",
                    "total_plus": 220,
                    "total_minus": 210,
                    "congress": 118,
                    "session": "2023",
                    "chamber": "house",
                    "link": "https://www.govtrack.us/congress/votes/118-2023/h123",
                },
            ],
            "meta": {"total_count": 1},
        }

        with patch("transparency_server._govtrack_get", new_callable=AsyncMock, return_value=api_data):
            from transparency_server import govtrack_votes
            result = await govtrack_votes()
            assert "Passage" in result or "passage" in result
            assert "220" in result or "Passed" in result


# --- World Bank Tests ---

class TestWorldBankIndicator:
    """Test worldbank_indicator tool."""

    @pytest.mark.asyncio
    async def test_returns_indicator_data(self, mock_response):
        """Returns formatted indicator data for a country."""
        # World Bank returns a list: [metadata, data_array]
        api_data = [
            {"page": 1, "pages": 1, "total": 2},
            [
                {
                    "indicator": {"id": "NY.GDP.MKTP.CD", "value": "GDP (current US$)"},
                    "country": {"id": "US", "value": "United States"},
                    "date": "2023",
                    "value": 25462700000000,
                },
                {
                    "indicator": {"id": "NY.GDP.MKTP.CD", "value": "GDP (current US$)"},
                    "country": {"id": "US", "value": "United States"},
                    "date": "2022",
                    "value": 25035164000000,
                },
            ],
        ]

        with patch("transparency_server._worldbank_get", new_callable=AsyncMock, return_value=api_data):
            from transparency_server import worldbank_indicator
            result = await worldbank_indicator(country="US", indicator="NY.GDP.MKTP.CD")
            assert "GDP" in result or "United States" in result
            assert "2023" in result

    @pytest.mark.asyncio
    async def test_no_data_available(self):
        """Returns message when no data available."""
        api_data = [{"page": 1, "pages": 0, "total": 0}, None]

        with patch("transparency_server._worldbank_get", new_callable=AsyncMock, return_value=api_data):
            from transparency_server import worldbank_indicator
            result = await worldbank_indicator(country="XX", indicator="FAKE.IND")
            assert "no data" in result.lower() or "not found" in result.lower()

    @pytest.mark.asyncio
    async def test_with_date_range(self):
        """Passes date range to API params."""
        api_data = [{"page": 1, "pages": 1, "total": 1}, [
            {"indicator": {"id": "X", "value": "X"}, "country": {"id": "US", "value": "US"}, "date": "2020", "value": 100}
        ]]

        with patch("transparency_server._worldbank_get", new_callable=AsyncMock, return_value=api_data) as mock_get:
            from transparency_server import worldbank_indicator
            result = await worldbank_indicator(country="US", indicator="NY.GDP.MKTP.CD", date_range="2020:2023")
            mock_get.assert_called_once()
            params = mock_get.call_args[1].get("params") or mock_get.call_args.kwargs.get("params", {})
            assert params.get("date") == "2020:2023"


class TestWorldBankSearch:
    """Test worldbank_search tool."""

    @pytest.mark.asyncio
    async def test_search_indicators(self, mock_response):
        """Returns matching indicators."""
        api_data = [
            {"page": 1, "pages": 1, "total": 2},
            [
                {"id": "NY.GDP.MKTP.CD", "name": "GDP (current US$)", "sourceNote": "GDP at purchaser prices..."},
                {"id": "NY.GDP.PCAP.CD", "name": "GDP per capita (current US$)", "sourceNote": "GDP per capita..."},
            ],
        ]

        with patch("transparency_server._worldbank_get", new_callable=AsyncMock, return_value=api_data) as mock_get:
            from transparency_server import worldbank_search
            result = await worldbank_search(query="GDP")
            mock_get.assert_called_once()
            assert mock_get.call_args[1].get("params", {}).get("q") == "GDP"
            assert "NY.GDP.MKTP.CD" in result
            assert "GDP" in result

    @pytest.mark.asyncio
    async def test_no_matching_indicators(self):
        """Returns message for no matches."""
        api_data = [{"page": 1, "pages": 0, "total": 0}, None]

        with patch("transparency_server._worldbank_get", new_callable=AsyncMock, return_value=api_data):
            from transparency_server import worldbank_search
            result = await worldbank_search(query="xyznonexistent")
            assert "no" in result.lower() or "0" in result


# --- ProPublica Nonprofit Explorer Tests ---

class TestNonprofitSearch:
    """Test nonprofit_search tool."""

    @pytest.mark.asyncio
    async def test_search_nonprofits(self, mock_response):
        """Returns formatted nonprofit search results."""
        api_data = {
            "total_results": 1,
            "organizations": [
                {
                    "ein": "131760110",
                    "name": "METROPOLITAN MUSEUM OF ART",
                    "city": "NEW YORK",
                    "state": "NY",
                    "ntee_code": "A51",
                    "total_revenue": 394836972,
                    "total_assets": 4183542218,
                },
            ],
        }

        with patch("transparency_server._propublica_get", new_callable=AsyncMock, return_value=api_data):
            from transparency_server import nonprofit_search
            result = await nonprofit_search(query="Metropolitan Museum")
            assert "METROPOLITAN" in result or "Metropolitan" in result
            assert "131760110" in result or "EIN" in result

    @pytest.mark.asyncio
    async def test_search_with_state_filter(self):
        """Passes state filter to API params."""
        api_data = {"total_results": 0, "organizations": []}

        with patch("transparency_server._propublica_get", new_callable=AsyncMock, return_value=api_data) as mock_get:
            from transparency_server import nonprofit_search
            result = await nonprofit_search(query="museum", state="NY")
            mock_get.assert_called_once()
            params = mock_get.call_args[1].get("params") or mock_get.call_args.kwargs.get("params", {})
            assert params.get("state[id]") == "NY"

    @pytest.mark.asyncio
    async def test_empty_search(self):
        """Returns no results message."""
        api_data = {"total_results": 0, "organizations": []}

        with patch("transparency_server._propublica_get", new_callable=AsyncMock, return_value=api_data):
            from transparency_server import nonprofit_search
            result = await nonprofit_search(query="xyznonexistent")
            assert "no" in result.lower() or "0" in result


class TestNonprofitDetails:
    """Test nonprofit_details tool."""

    @pytest.mark.asyncio
    async def test_returns_org_details(self, mock_response):
        """Returns formatted org details with filing data."""
        api_data = {
            "organization": {
                "ein": "131760110",
                "name": "METROPOLITAN MUSEUM OF ART",
                "city": "NEW YORK",
                "state": "NY",
                "ntee_code": "A51",
                "subsection_code": 3,
                "ruling_date": "1940-07-01",
                "tax_period": 202206,
                "asset_amount": 4183542218,
                "income_amount": 394836972,
            },
            "filings_with_data": [
                {
                    "tax_prd": "202206",
                    "tax_prd_yr": "2022",
                    "totrevenue": 394836972,
                    "totfuncexpns": 359543821,
                    "totassetsend": 4183542218,
                    "totliabend": 1064958473,
                    "pct_compnsatncurrofcr": 0.05,
                },
            ],
            "filings_without_data": [],
        }

        with patch("transparency_server._propublica_get", new_callable=AsyncMock, return_value=api_data):
            from transparency_server import nonprofit_details
            result = await nonprofit_details(ein="131760110")
            assert "METROPOLITAN" in result
            assert "131760110" in result
            assert "revenue" in result.lower() or "394" in result

    @pytest.mark.asyncio
    async def test_invalid_ein(self):
        """Returns error for invalid EIN."""
        with patch("transparency_server._propublica_get", new_callable=AsyncMock, side_effect=httpx.HTTPStatusError("404", request=MagicMock(), response=MagicMock(status_code=404))):
            from transparency_server import nonprofit_details
            result = await nonprofit_details(ein="000000000")
            assert "error" in result.lower() or "not found" in result.lower()


# --- Status Tool Tests ---

class TestTransparencyStatus:
    """Test transparency_status connectivity check."""

    @pytest.mark.asyncio
    async def test_all_apis_up(self, mock_response):
        """Reports all APIs as connected."""
        govtrack_resp = mock_response(json_data={"meta": {"total_count": 0}, "objects": []})
        worldbank_resp = mock_response(json_data=[{"page": 1}, []])
        propublica_resp = mock_response(json_data={"total_results": 0, "organizations": []})

        async def mock_get(url, **kwargs):
            if "govtrack" in url:
                return govtrack_resp
            elif "worldbank" in url:
                return worldbank_resp
            elif "propublica" in url:
                return propublica_resp
            return mock_response(status_code=500)

        mock_client = AsyncMock()
        mock_client.get = mock_get
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)

        with patch("httpx.AsyncClient", return_value=mock_client):
            from transparency_server import transparency_status
            result = await transparency_status()
            assert "govtrack" in result.lower()
            assert "world bank" in result.lower() or "worldbank" in result.lower()
            assert "propublica" in result.lower()

    @pytest.mark.asyncio
    async def test_api_down(self, mock_response):
        """Reports unreachable API."""
        async def mock_get(url, **kwargs):
            if "govtrack" in url:
                raise httpx.ConnectError("Connection refused")
            return mock_response(json_data={})

        mock_client = AsyncMock()
        mock_client.get = mock_get
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)

        with patch("httpx.AsyncClient", return_value=mock_client):
            from transparency_server import transparency_status
            result = await transparency_status()
            assert "error" in result.lower() or "unreachable" in result.lower() or "failed" in result.lower()


# --- Helper Function Tests ---

class TestHelpers:
    """Test internal helper functions."""

    @pytest.mark.asyncio
    async def test_govtrack_get(self, mock_response):
        """_govtrack_get calls correct URL and returns JSON."""
        resp = mock_response(json_data={"objects": [], "meta": {"total_count": 0}})

        mock_client = AsyncMock()
        mock_client.get = AsyncMock(return_value=resp)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)

        with patch("httpx.AsyncClient", return_value=mock_client):
            from transparency_server import _govtrack_get
            result = await _govtrack_get("role", params={"current": "true"})
            assert result == {"objects": [], "meta": {"total_count": 0}}

    @pytest.mark.asyncio
    async def test_worldbank_get(self, mock_response):
        """_worldbank_get calls correct URL and returns JSON."""
        resp = mock_response(json_data=[{"page": 1}, []])

        mock_client = AsyncMock()
        mock_client.get = AsyncMock(return_value=resp)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)

        with patch("httpx.AsyncClient", return_value=mock_client):
            from transparency_server import _worldbank_get
            result = await _worldbank_get("country/US/indicator/NY.GDP.MKTP.CD")
            assert isinstance(result, list)

    @pytest.mark.asyncio
    async def test_propublica_get(self, mock_response):
        """_propublica_get calls correct URL and returns JSON."""
        resp = mock_response(json_data={"total_results": 0, "organizations": []})

        mock_client = AsyncMock()
        mock_client.get = AsyncMock(return_value=resp)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)

        with patch("httpx.AsyncClient", return_value=mock_client):
            from transparency_server import _propublica_get
            result = await _propublica_get("search.json", params={"q": "test"})
            assert "total_results" in result


# --- Data Formatting Tests ---

class TestDataFormatting:
    """Test that tools return structured, useful output — not raw API dumps."""

    @pytest.mark.asyncio
    async def test_member_formatting_includes_key_fields(self):
        """Member output includes name, party, state, role."""
        api_data = {
            "objects": [
                {
                    "person": {
                        "firstname": "John",
                        "lastname": "Smith",
                        "birthday": "1970-01-01",
                        "gender": "male",
                        "link": "https://govtrack.us/congress/members/john_smith/12345",
                    },
                    "role_type": "senator",
                    "state": "TX",
                    "party": "Republican",
                    "startdate": "2023-01-03",
                    "enddate": "2025-01-03",
                },
            ],
            "meta": {"total_count": 1},
        }

        with patch("transparency_server._govtrack_get", new_callable=AsyncMock, return_value=api_data):
            from transparency_server import govtrack_members
            result = await govtrack_members(state="TX")
            # Must contain all key fields — a mutation removing any should fail
            assert "John" in result
            assert "Smith" in result
            assert "TX" in result
            assert "Republican" in result
            assert "senator" in result.lower() or "Senator" in result

    @pytest.mark.asyncio
    async def test_bill_formatting_includes_key_fields(self):
        """Bill output includes title, status, congress, bill number."""
        api_data = {
            "objects": [
                {
                    "title": "Test Act of 2024",
                    "bill_type": "senate_bill",
                    "number": 42,
                    "congress": 118,
                    "current_status": "passed_bill",
                    "introduced_date": "2024-01-15",
                    "link": "https://www.govtrack.us/congress/bills/118/s42",
                },
            ],
            "meta": {"total_count": 1},
        }

        with patch("transparency_server._govtrack_get", new_callable=AsyncMock, return_value=api_data):
            from transparency_server import govtrack_bills
            result = await govtrack_bills(query="test")
            assert "Test Act" in result
            assert "118" in result or "s42" in result.lower()
            assert "passed" in result.lower()

    @pytest.mark.asyncio
    async def test_worldbank_nonmonetary_no_dollar_sign(self):
        """Non-monetary World Bank indicators should not have $ prefix."""
        api_data = [
            {"page": 1, "pages": 1, "total": 1},
            [
                {
                    "indicator": {"id": "SP.POP.TOTL", "value": "Population, total"},
                    "country": {"id": "US", "value": "United States"},
                    "date": "2023",
                    "value": 331900000,
                },
            ],
        ]

        with patch("transparency_server._worldbank_get", new_callable=AsyncMock, return_value=api_data):
            from transparency_server import worldbank_indicator
            result = await worldbank_indicator(country="US", indicator="SP.POP.TOTL")
            assert "Population" in result
            # Non-monetary: should NOT have dollar sign
            assert "$" not in result

    @pytest.mark.asyncio
    async def test_worldbank_monetary_has_dollar_sign(self):
        """Monetary World Bank indicators should have $ prefix."""
        api_data = [
            {"page": 1, "pages": 1, "total": 1},
            [
                {
                    "indicator": {"id": "NY.GDP.MKTP.CD", "value": "GDP (current US$)"},
                    "country": {"id": "US", "value": "United States"},
                    "date": "2023",
                    "value": 25462700000000,
                },
            ],
        ]

        with patch("transparency_server._worldbank_get", new_callable=AsyncMock, return_value=api_data):
            from transparency_server import worldbank_indicator
            result = await worldbank_indicator(country="US", indicator="NY.GDP.MKTP.CD")
            assert "$" in result

    @pytest.mark.asyncio
    async def test_nonprofit_formatting_includes_financials(self):
        """Nonprofit output includes EIN, name, and revenue/asset data."""
        api_data = {
            "total_results": 1,
            "organizations": [
                {
                    "ein": "123456789",
                    "name": "TEST FOUNDATION",
                    "city": "CHICAGO",
                    "state": "IL",
                    "ntee_code": "T20",
                    "total_revenue": 50000000,
                    "total_assets": 200000000,
                },
            ],
        }

        with patch("transparency_server._propublica_get", new_callable=AsyncMock, return_value=api_data):
            from transparency_server import nonprofit_search
            result = await nonprofit_search(query="test foundation")
            assert "TEST FOUNDATION" in result
            assert "123456789" in result
            # Financial data should be human-readable
            assert "50" in result or "revenue" in result.lower()
