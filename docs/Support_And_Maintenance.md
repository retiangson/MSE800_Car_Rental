# Support & Maintenance of Car Rental System

This plan discusses steps that will keep all of the software, hardware and processes utilized to run the Car Rental System up to date over its lifecycle.

---

## 1. Software Maintenance Management

**Layered Architecture**
It allows you to break down each system into UI layer, Business Layer, Domain Layers and Data layers so that with minimal impact the components can be updated without much impact on the application as a whole.

**Bug Fixes**
Defects can be addressed in their seprare layer (for example fixing validation in RentalService does not touch the database logic).

**Documentation**
Good documentation – such as User Guides, System Documentation, UML diagrams and Coding Standards all assist the new developer to slot into the development process faster.

**Testing**
Unit tests, in the pytest format, make it difficult for developers to break features with refactoring.

Together, these practices provide a solid basis for the long-term maintenance of software.

---

## 2. Versioning

The project follows the guidelines of Semantic Versioning (SemVer):

* **MAJOR version** - when you make incompatible API changes, or very rarely for structural changes that break backwards compatibility.
* **MINOR version** – when you add functionality in a backwards compatible manner.
* **PATCH version** - for fixing bugs and making small improvements.

**Example versions:**

* v1. 0. 0 – Initial stable release
* v1. 1. 0 - new feature (rental fee calculator or any other)
* v1. 1. 1- Fixed a bug

Each version is well marked with a tag for easy tracking in github.

---

## 3. Backward Compatibility

To be compatible with prior versions as the system changes:

**DTOs and Mappers**
DTO acts as a middleware layer between the internal db and your external interfaces (UI, API), protecting them from changes in the internal storage.

**Database Migration Strategy**
Schema changes will be managed with Alembic to enable controlled and incremental upgrades without any loss of data.

**API Stability**
Older versions will continue to be available in case RESTful endpoints are added (for instance, via FastAPI) as well, and users can transition.

**Deprecation Policy**
Deprecated features shall be documented explicitly and supported for at least one minor release before removal.

This method enables contiuing use of an old terminal even when new functionalities are developed.

---

## Summary

Car Rental System is designed for sustainability in the long term:

* Maintenance is straightforward as a modular structure and comprehensive documentation has been utilized.
* SemVer is employed for versioning in a straightforward, senseful manner.
* It maintains compatibility through protective data layers, cautious database migrations and thoughtful deprecation policies.

All of the major components discussed on the rubric will be addressed in this plan to help keep your system maintainable, extensible, and reliable.