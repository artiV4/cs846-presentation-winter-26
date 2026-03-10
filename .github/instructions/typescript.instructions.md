---
applyTo: "**/*.ts"
---
# TypeScript Coding Standards
This file defines our TypeScript coding conventions for Copilot code review.
## Naming Conventions
- Use camelCase for variables and functions.
- Use PascalCase for classes and interfaces.
- Use UPPER_CASE for constants.

## Code Style
- Prefer explicit types for function parameters and return values.
- Use single quotes for strings.
- Indent with 2 spaces.
- Avoid trailing whitespace.
- Keep functions short and focused.

## Error Handling
- Always handle errors explicitly (try/catch, error callbacks).
- Never swallow errors silently.
- Provide meaningful error messages.

## Testing
- Write unit tests for all public functions and classes.
- Cover edge cases and error conditions.
- Use descriptive test names.

## Example
```typescript
// Good
function getUser(id: string): User | null {
  if (!id) throw new Error('Invalid user id');
  // ...existing code...
}

// Bad
function getuser(id) {
  // no error handling
  // ...existing code...
}
```
