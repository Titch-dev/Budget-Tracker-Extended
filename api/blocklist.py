"""
blocklist.py

Contains the blocklist of JWT tokens. Imported by app and the logout resource
so tokens can be added when the user logs out.
"""

BLOCKLIST = set()