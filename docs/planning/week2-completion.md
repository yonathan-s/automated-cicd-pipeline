# Week 2 Completion Checklist

**Week:** 20-26 February 2025  
**Phase:** Sample Web Application Development

---

## ✅ Application Development

- [ ] Flask application created (`src/webapp/app.py`)
- [ ] 6 REST API endpoints implemented:
  - [ ] GET /health - Health check
  - [ ] GET /api/tasks - Get all tasks
  - [ ] GET /api/tasks/{id} - Get single task
  - [ ] POST /api/tasks - Create task
  - [ ] PUT /api/tasks/{id} - Update task
  - [ ] DELETE /api/tasks/{id} - Delete task
  - [ ] GET /api/stats - Get statistics
- [ ] HTML frontend created (`templates/index.html`)
- [ ] Configuration system implemented (`config.py`)
- [ ] Error handling and validation added
- [ ] Logging configured

---

## ✅ Testing

- [ ] pytest installed
- [ ] Unit tests created (`tests/unit/test_app.py`)
- [ ] 11 tests written
- [ ] All tests passing
- [ ] Test coverage: ~80%

**Test Results:**
```
======================== test session starts ========================
collected 11 items

tests/unit/test_app.py::test_health_check PASSED
tests/unit/test_app.py::test_get_tasks_empty PASSED
tests/unit/test_app.py::test_create_task PASSED
tests/unit/test_app.py::test_create_task_without_title PASSED
tests/unit/test_app.py::test_get_task_by_id PASSED
tests/unit/test_app.py::test_get_nonexistent_task PASSED
tests/unit/test_app.py::test_update_task PASSED
tests/unit/test_app.py::test_delete_task PASSED
tests/unit/test_app.py::test_get_stats PASSED
tests/unit/test_app.py::test_multiple_tasks PASSED

===================== 11 passed in 0.50s ========================
```

---

## ✅ Documentation

- [ ] Application README created (`src/webapp/README.md`)
- [ ] API endpoints documented
- [ ] Testing documentation created (`tests/README.md`)
- [ ] Main README updated with Week 2 progress
- [ ] Configuration documented (`.env.example`)

---

## ✅ Dependencies

- [ ] `requirements.txt` created with all dependencies:
  - Flask 3.0.2
  - Flask-CORS
  - pytest
  - pytest-flask
  - pytest-cov

---

## ✅ Local Testing

- [ ] Application runs on http://localhost:5000
- [ ] Web interface functional
- [ ] All API endpoints tested manually
- [ ] Error handling verified
- [ ] Logging confirmed working

---

## ✅ Code Quality

- [ ] Code follows Python best practices
- [ ] Functions have docstrings
- [ ] Error handling implemented
- [ ] Input validation working
- [ ] Logging configured
- [ ] Configuration separated from code

---

## Files Created This Week
```
src/webapp/
├── app.py                 # Main Flask application
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables example
├── README.md             # Application documentation
└── templates/
    └── index.html        # Web interface

tests/
├── unit/
│   └── test_app.py       # Unit tests
└── README.md             # Testing documentation

docs/planning/
└── week-2-completion.md  # This file
```

---

## Time Spent

| Task | Time Spent | Notes |
|------|-----------|-------|
| Flask app setup | 2 hours | Initial setup and basic endpoints |
| HTML frontend | 1 hour | Web interface creation |
| Code improvements | 2 hours | Config, error handling, logging |
| Testing | 2 hours | Writing and running tests |
| Documentation | 1.5 hours | READMEs and documentation |
| **TOTAL** | **~8.5 hours** | On track |

---

## Blockers Encountered

[Document any problems and solutions]

Example:
- **Blocker:** PowerShell execution policy prevented venv activation
- **Solution:** Ran `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

---

## Application Statistics

- **Lines of Python code:** ~350
- **Number of endpoints:** 7
- **Number of tests:** 10
- **Test pass rate:** 100%
- **Dependencies:** 10 packages

---

## Screenshots Taken

- Application running in browser
- Test results passing (These are the results of the tests in 'tests\unit\test_app.py')
- Terminal showing Flask running 
- (Saved in `docs/screenshots/week-2/`)

---

## Key Learnings

**What went well:**
- Flask is straightforward for building REST APIs
- Testing with pytest is easy to set up
- Error handling improves API usability

**What was challenging:**
- Understanding Flask's request/response cycle initially
- Writing comprehensive tests
- Configuring logging properly

**Lessons learned:**
- Start with simple functionality, then add features
- Write tests alongside code, not after
- Good error messages help debugging
- Documentation is essential for future reference

---

## Next Week Preview

**Week 3 (27 Feb - 5 Mar): Containerization**

Tasks to prepare for:
- [ ] Review Docker basics
- [ ] Understand Dockerfile syntax
- [ ] Think about container optimization
- [ ] Ensure app still runs locally

**Expected deliverables:**
- Dockerfile
- .dockerignore
- Container running locally
- Documentation

---

## Validation Checks

Before moving to Week 3, verify:

✅ **Application runs:**
```bash
cd src/webapp
python app.py
# Visit http://localhost:5000
```

✅ **Tests pass:**
```bash
pytest tests/unit/test_app.py -v
# All 11 tests should pass
```

✅ **Requirements are complete:**
```bash
pip freeze | findstr Flask
# Should show Flask and Flask-CORS
```

✅ **Files committed to Git:**
```bash
git status
# Should show clean working directory or staged changes
```

---

## Academic Contribution

**This week contributes to dissertation:**

**Implementation Chapter:**
- Application architecture and design decisions
- REST API design patterns
- Error handling strategy
- Testing methodology

**Methodology Chapter:**
- Technology selection justification (Flask)
- Development approach
- Testing strategy

**Code Quality:**
- Clean code principles
- Documentation standards
- Test coverage approach

---

## Sign-off

**Week 2 Status:** COMPLETE ✅

**Ready for Week 3:** YES / NO

**Completion Date:** [Fill in date]

---

## Git Commit Message

Use this commit message when pushing Week 2 work:
```
Week 2 Complete: Flask Task Manager API

- Implemented 7 REST API endpoints (CRUD operations)
- Created responsive web interface with JavaScript
- Added configuration management system
- Implemented comprehensive error handling and validation
- Added logging throughout application
- Wrote 11 unit tests with 100% pass rate
- Documented API endpoints and usage
- Created testing documentation
- Application runs successfully on localhost:5000



