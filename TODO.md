# TODO: Add Location Button with Local Resource Numbers

## Plan:
- [ ] Update backend (app.py) to accept location parameter and return local resources
- [ ] Update frontend (App.js) to add location selector
- [ ] Test the implementation

## Details:
1. Backend changes:
   - Add `location` parameter to ChatRequest
   - Load local_resources.json
   - Return local resources when location is provided

2. Frontend changes:
   - Add location state
   - Add location selector dropdown/buttons in chat interface
   - Send location with message to backend
