#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 12:45:49 2025

@author: mac2
"""

import argparse
import os

def scrape(config_path, folder, browser, name, print_logs, debug, verbose):
    """ main logique """
    print(f"Running scraper with config: {config_path}")
    print(f"Saving data to: {folder}")
    print(f"Using browser: {browser}")
    print(f"Project name: {name}")
    if print_logs:
        print("Logs will be printed")
    if debug:
        print("Debug mode ON")
    if verbose:
        print("Verbose output enabled")

    
    print("Scraping data... Done!")

def main():
    parser = argparse.ArgumentParser(description="Run the web scraper for Panerai watches.")
    parser.add_argument("config_path", help="Path to the config YAML file")
    parser.add_argument("--folder", default="./data", help="Folder to save the data")
    parser.add_argument("--browser", default="chrome", choices=["chrome", "firefox"], help="Browser to use")
    parser.add_argument("--name", default="panerai_all", help="Project name")
    parser.add_argument("-p", "--print_logs", action="store_true", help="Print logs")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()
    scrape(args.config_path, args.folder, args.browser, args.name, args.print_logs, args.debug, args.verbose)

if __name__ == "__main__":
    main()
