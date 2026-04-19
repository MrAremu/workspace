# Google OAuth Setup Guide

It seems like you are encountering a `redirect_uri_mismatch` error. This usually happens when the **Application Type** in Google Cloud Console is set to "Web Application" but the local script is behaving like a Desktop app, or the ports don't match exactly.

## Recommended Fix: Use "Desktop App" Client Type

This is the easiest and most robust way for local scripts.

1.  Go to the [Google Cloud Console Credentials Page](https://console.cloud.google.com/apis/credentials).
2.  Click **+ CREATE CREDENTIALS** > **OAuth client ID**.
3.  **Application type**: Select **Desktop app**.
    *   *If you don't see this option, ensure you have configured the OAuth Consent Screen as "External" (or "Internal" if you are in a Workspace).*
4.  Name it "Local Python Scripts" or similar.
5.  Click **CREATE**.
6.  **Download JSON** (the download icon on the right).
7.  Rename this file to `credentials.json` and replace the one in your `Workspace` folder.
8.  **Delete `token.pickle`** if it exists (so we can re-authenticate).

---

## Alternative: Using "Web Application" (Harder)

If you must use the "Web Application" type:

1.  Go to your existing OAuth Client ID in the Console.
2.  Under **Authorized redirect URIs**, execute:
    *   Add: `http://localhost:8080/`
    *   *Note: It must be exact. No trailing slash mismatch, no http vs https.*
3.  Save.
4.  Ensure `execution/google_service_auth.py` is using `port=8080` (I can set this for you).
5.  Replace `credentials.json` with the latest version just in case.

## Summary
I recommend the **Desktop App** approach. It allows dynamic ports (`port=0`) which handles standard `http://localhost:<random>/` redirects automatically without manual configuration.
