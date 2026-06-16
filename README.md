# RSP PartMatch AI

Internal procurement and inside-sales support API for finding approved replacement/substitute parts for industrial/electrical components.

## Goal

Help RSP Supply co-workers quickly find approved substitute options while helping customers, especially over the phone. The backend supports a browser extension popup that can accept a part number, manufacturer, or product details and return structured replacement information.

## Current Scope

- FastAPI backend
- Browser-extension-friendly search endpoint
- Chrome/Edge extension popup scaffold
- Request/response schemas
- Approved vendor loading service
- Original product fixture lookup
- Substitute candidate validation
- Spec comparison table
- Customer-ready response summary
- Approved vendor list endpoint

## API

### Health Check

`GET /health`

### Browser Extension Search

`POST /api/v1/search`

Preferred endpoint for the extension popup.

Example exact-part request:

```json
{
  "part_number": "ENCJK",
  "manufacturer": "nVent Hoffman"
}
```

Example product-details request:

```json
{
  "product_details": "stainless steel enclosure 20 x 16 x 8"
}
```

Response includes:

- `search` metadata
- `original_part`
- approved `substitutes`
- `comparison_table`
- `recommendation_status`
- `customer_ready_response`

### Backward-Compatible Substitute Search

`POST /substitutes`

This currently uses the same backend flow as `/api/v1/search`.

### Approved Vendors

`GET /api/v1/vendors/approved`

Returns the approved vendor list loaded from `data/approved_vendors.json`.

## Browser Extension Popup

A Chrome/Edge extension scaffold lives in:

```text
extension/
```

Load it with Chrome/Edge Developer Mode using **Load unpacked** and selecting the `extension` folder.

The popup opens from the normal browser toolbar area in the top-right, calls `POST /api/v1/search`, and displays approved matches quickly.

## Development

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the API:

```bash
uvicorn app.main:app --reload
```

Open docs:

- http://127.0.0.1:8000/docs

Run tests:

```bash
python -m pytest -q
```

Expected current result:

```text
16 passed
```

## Important Business Rules

- Substitute vendors must be approved vendors only.
- Do not recommend used, refurbished, repaired, or unknown-condition products.
- Part numbers must be matched exactly in the current fixture-backed phase.
- Each substitute must include a valid product URL.
- Match percentages below 70% should not be recommended.
- Accuracy is more important than speed.
