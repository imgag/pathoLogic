# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Add delete button and make it possible to delete and restart in the frontend.
- Add logout button

### Change
- Create a virtual file and download it with access token

### Removed
- Remove status_get_id controller because it was not used in the project

## [0.2.0] - 2019-07-30
### Added
- Added Uppy Dashboard + XHR based file upload
- Add controller to upload files
- Added login to frontend using fetchDefaults and oauth2-client-js
- Add JWT based authentication schema
- Add JWT implementation and requirements

### Changed
- Enforce JWT on API side
- Only return results by user ID
- Replace file input with selects in sample creation
- Use correct path (user path) to write TSV

### Fixed
- Correctly verify the create samples form

### Removed
- Remove author_email field as it is redundant and slows down the user

## [0.1.2] - 2019-04-15
### Added

- OpenAPI based API and schema
- frontend in Vue + Vuetify
- install instructions and installer script for plasmIdent and hybridassembly

