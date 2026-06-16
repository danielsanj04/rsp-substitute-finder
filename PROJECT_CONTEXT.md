# RSP PartMatch AI — Project Context

_Last updated: 2026-06-04 12:48 MDT_

## Updated Project Purpose

The purpose of **RSP PartMatch AI** is to make it easier for RSP Supply co-workers to find replacement or substitute parts during their daily work, especially while helping customers over the phone.

Currently, team members often need to open many browser tabs, search multiple vendor websites, compare specifications manually, and check whether a vendor is approved before giving customers an answer.

This project will solve that problem by creating a **browser extension** that opens as a small popup. The user can type in a part number, manufacturer, or product details, and the tool will return the best approved replacement options.

The extension should help users quickly find:

- The original part information
- Approved substitute parts
- Product descriptions
- Key specification comparisons
- Stock availability
- Vendor links
- A short customer-ready response

## Goal

Reduce search time, simplify the workflow, and help co-workers respond to customers faster and more accurately.

## Working Product Direction

- Primary user interface: browser extension popup
- User input: part number, manufacturer, or product details
- Output: approved replacement/substitute options with supporting details
- Backend role: search, validate, compare, and format results
- Frontend role: lightweight popup experience for co-workers during customer calls

## Core Rules / Constraints

- Recommended substitute parts must come from approved vendors.
- Approved vendors should be validated against `Vendor Cheat Sheet (1).pdf`.
- Do not recommend used, refurbished, repaired, or unknown-condition items.
- Part numbers should be handled carefully; exact matches matter.
- Poor matches below the confidence threshold should not be recommended.
- The tool should help users answer customers quickly, but accuracy is more important than speed.

## Desired Result Fields

For each search, the tool should aim to return:

- Original part information
- Approved substitute part(s)
- Manufacturer/vendor
- Product description
- Key specifications
- Specification comparison against the requested/original part
- Stock availability
- Vendor/source link
- Confidence or match quality
- Short customer-ready response

## Current Known Project Path

`/Users/danielsj/Documents/RSP Supply Projects/RSP Substitute Finder`

## Current Backend API Contract

### `POST /api/v1/search`

Preferred browser extension search endpoint.

Accepts at least one of:

- `part_number`
- `manufacturer`
- `product_details`

Returns:

- `search` metadata
- `original_part`
- approved `substitutes`
- `comparison_table`
- `recommendation_status`
- `customer_ready_response`
- `sales_email_summary` backward-compatible alias

### `POST /substitutes`

Backward-compatible endpoint using the same substitute search flow.

### `GET /api/v1/vendors/approved`

Returns the approved vendor list loaded from `data/approved_vendors.json`.

## Notes for Future Development

This context supersedes the earlier idea of only building a backend substitute finder. The product should now be thought of as a full workflow tool:

1. Browser extension popup for co-workers
2. Backend API for search and validation
3. Vendor approval checking
4. Substitute comparison logic
5. Customer-ready response generation
