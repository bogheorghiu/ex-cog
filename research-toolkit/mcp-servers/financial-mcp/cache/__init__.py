"""
Cache module for MCP servers.
Provides persistent caching capabilities using SQLite.
"""

from .manager import CacheManager

__all__ = ['CacheManager']