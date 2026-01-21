#!/usr/bin/env python3
"""
Setup script for PitchForge AI
Helps users configure their environment variables interactively.
"""

import os
import sys


def create_env_file():
    """Interactive setup to create .env file from .env.example"""
    
    print("=" * 60)
    print("PitchForge AI - Environment Setup")
    print("=" * 60)
    print()
    
    # Check if .env already exists
    if os.path.exists(".env"):
        response = input(".env file already exists. Overwrite? (y/N): ").strip().lower()
        if response != 'y':
            print("Setup cancelled.")
            return
    
    # Check if .env.example exists
    if not os.path.exists(".env.example"):
        print("Error: .env.example not found!")
        print("Please ensure you're running this script from the project root.")
        sys.exit(1)
    
    print("This script will help you create your .env file.")
    print("Press Enter to use the default value shown in brackets.\n")
    
    # Required fields
    required_fields = {
        "TEMPLATE_PRESENTATION_ID": {
            "prompt": "Google Slides Template ID",
            "help": "Find this in your Google Slides URL after /d/"
        },
        "COMPANY_NAME": {
            "prompt": "Company Name",
            "help": "Your company or project name"
        }
    }
    
    env_values = {}
    
    # Get required fields
    print("Required Configuration:")
    print("-" * 60)
    for key, info in required_fields.items():
        while True:
            value = input(f"{info['prompt']}: ").strip()
            if value:
                env_values[key] = value
                break
            else:
                print(f"  ℹ {info['help']}")
                print("  This field is required. Please enter a value.\n")
    
    print("\n" + "=" * 60)
    response = input("Do you want to customize all other fields now? (y/N): ").strip().lower()
    
    if response == 'y':
        print("\nPlease edit the .env file manually to customize all fields.")
        print("Use .env.example as a reference.\n")
    
    # Copy .env.example and update required fields
    with open(".env.example", "r") as f:
        content = f.read()
    
    # Replace required fields
    for key, value in env_values.items():
        # Find and replace the line
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith(f"{key}="):
                lines[i] = f"{key}={value}"
        content = '\n'.join(lines)
    
    # Write .env file
    with open(".env", "w") as f:
        f.write(content)
    
    print("=" * 60)
    print("✓ .env file created successfully!")
    print()
    print("Next steps:")
    print("1. Edit .env to customize all fields for your pitch deck")
    print("2. Ensure oauth_credentials.json is in the project root")
    print("3. Run: python generate_ppt.py")
    print("=" * 60)


if __name__ == "__main__":
    try:
        create_env_file()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)
