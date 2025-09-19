
| Section | 	Content                                                       |
|:---------------------------------------------------|:---------------------------------------------------------------|
| API Explanation	| This endpoint retrieves a single user's profile information... |
| Happy Path	| - Retrieve an existing user with a valid ID...                 |
| Unhappy Path	| - Request a user with a non-existent ID...<br>- Request a user with an invalid ID...<br>- **(NEW)** Verify the response does not contain sensitive, non-public user data (e.g., password hash, home address). |
| Edge Cases	| - Request a user with the lowest possible valid ID (e.g., 1). |
