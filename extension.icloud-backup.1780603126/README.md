# RSP PartMatch AI Browser Extension

Chrome/Edge extension popup for quickly searching approved substitute parts.

## What it does

- Opens from the browser toolbar in the normal top-right extension popup area.
- Lets the user type a part number, manufacturer, or product details.
- Calls the backend search endpoint: `POST /api/v1/search`.
- Shows the original part, best approved substitute, key specs, stock/vendor info, and customer-ready response.

## Local API

By default, `popup.js` calls:

```text
http://127.0.0.1:8000/api/v1/search
```

It also has a temporary fallback for the current preview server:

```text
http://127.0.0.1:8011/api/v1/search
```

Once the real FastAPI backend is consistently running on port `8000`, the fallback can be removed.

## Load in Chrome or Edge

1. Open Chrome/Edge.
2. Go to `chrome://extensions` or `edge://extensions`.
3. Enable **Developer mode**.
4. Click **Load unpacked**.
5. Select this folder:

```text
/Users/danielsj/Documents/RSP Supply Projects/RSP Substitute Finder/extension
```

6. Pin **RSP PartMatch AI** to the toolbar.
7. Click the extension icon and search for:

```text
ENCJK nVent Hoffman
```

## Current sample behavior

Known sample match:

- Input: `ENCJK nVent Hoffman`
- Expected result: approved Grainger match, 100%, New, In Stock

Unknown sample:

- Input: `A20H1608SSLP Hoffman`
- Expected result: no approved substitute found yet
