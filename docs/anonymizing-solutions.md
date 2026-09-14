# Anonymizing example solutions

The safest fixture is one created specifically for testing. Do not assume that replacing a flow display name is sufficient.

Before sharing an export, inspect all text files for:

- tenant and SharePoint URLs;
- email addresses and user names;
- environment, list, library and site identifiers;
- connection reference names;
- application, subscription and directory IDs;
- sample business data;
- API keys, tokens, passwords and webhook URLs.

Replace values with deterministic examples such as:

- `https://contoso.sharepoint.com/sites/example`
- `maker@example.invalid`
- `00000000-0000-0000-0000-000000000000`

Then extract the ZIP and search the full directory again. If you cannot confidently establish that the fixture is safe to publish, recreate the scenario synthetically.
