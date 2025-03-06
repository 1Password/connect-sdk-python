#!/usr/bin/env python3
"""
Example script demonstrating how to connect to a 1Password Connect server
using CA certificate verification and list all secrets in a vault.

Shows both synchronous and asynchronous usage.
Update the configuration variables below with your values.
"""

import asyncio
from onepasswordconnectsdk.client import new_client
from onepasswordconnectsdk.config import ClientConfig

# Configuration
CONNECT_URL = "https://connect.example.com"  # Your 1Password Connect server URL
TOKEN = "eyJhbGc..."                         # Your 1Password Connect token
VAULT_ID = "vaults_abc123"                   # ID of the vault to list secrets from
CA_FILE = "path/to/ca.pem"                   # Path to your CA certificate file

def list_vault_secrets():
    """
    Connect to 1Password Connect server and list all secrets in the specified vault.
    Uses CA certificate verification for secure connection.
    """
    try:
        # Configure client with CA certificate verification
        config = ClientConfig(
            ca_file=CA_FILE,
            timeout=30.0  # 30 second timeout
        )
        
        # Initialize client with configuration
        client = new_client(CONNECT_URL, TOKEN, config=config)
        
        # Get all items in the vault
        items = client.get_items(VAULT_ID)
        
        # Print items
        print(f"\nSecrets in vault {VAULT_ID}:")
        print("-" * 40)
        for item in items:
            print(f"- {item.title} ({item.category})")
            
    except Exception as e:
        print(f"Error: {str(e)}")


async def list_vault_secrets_async():
    """
    Async version: Connect to 1Password Connect server and list all secrets in the specified vault.
    Uses CA certificate verification for secure connection.
    """
    try:
        # Configure client with CA certificate verification
        config = ClientConfig(
            ca_file=CA_FILE,
            timeout=30.0  # 30 second timeout
        )
        
        # Initialize async client with configuration
        client = new_client(CONNECT_URL, TOKEN, is_async=True, config=config)
        
        # Get all items in the vault
        items = await client.get_items(VAULT_ID)
        
        # Print items
        print(f"\nSecrets in vault {VAULT_ID} (async):")
        print("-" * 40)
        for item in items:
            print(f"- {item.title} ({item.category})")
            
        # Close the client gracefully
        await client.session.aclose()
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    # Run sync version
    print("Running synchronous example...")
    list_vault_secrets()
    
    # Run async version
    print("\nRunning asynchronous example...")
    asyncio.run(list_vault_secrets_async())
