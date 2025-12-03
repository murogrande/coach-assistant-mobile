# GitHub Issues for Mobile Repository

Copy each issue below to create on GitHub after pushing the repository.

---

## Issue #1: Setup KivyMD Project Configuration

**Labels**: `setup`, `high-priority`

**Description**:

Configure the basic KivyMD application structure and theme.

**Tasks**:
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Configure app theme in `main.py`:
  - [ ] Set primary color palette
  - [ ] Set accent color
  - [ ] Set theme style (Light/Dark)
- [ ] Create basic screen manager
- [ ] Add app icon (placeholder)
- [ ] Test app runs on desktop: `python main.py`
- [ ] Create basic navigation structure

**Acceptance Criteria**:
- App launches without errors
- Theme colors applied correctly
- Screen manager working
- Basic navigation functional

**Estimated Time**: 1-2 hours

---

## Issue #2: Implement Login Screen UI

**Labels**: `frontend`, `ui`, `high-priority`

**Description**:

Create the login and registration screen UI.

**Tasks**:
- [ ] Create `screens/login.py`
- [ ] Create login UI:
  - [ ] Username text field
  - [ ] Password text field (obscured)
  - [ ] Login button
  - [ ] Register button
  - [ ] App logo/title
- [ ] Add input validation:
  - [ ] Required fields
  - [ ] Minimum password length
- [ ] Add loading indicator
- [ ] Add error message display
- [ ] Test UI on desktop

**Acceptance Criteria**:
- Login screen displays correctly
- Input fields work properly
- Validation shows errors
- UI follows Material Design guidelines

**Estimated Time**: 2-3 hours

---

## Issue #3: Implement Authentication Logic

**Labels**: `frontend`, `api`, `high-priority`

**Description**:

Connect login screen to backend API and handle authentication.

**Tasks**:
- [ ] Update `API_BASE_URL` in `services/api_client.py`
- [ ] Implement login button handler:
  - [ ] Call `api_client.login()`
  - [ ] Show loading indicator
  - [ ] Handle success (save token, navigate to home)
  - [ ] Handle errors (show error message)
- [ ] Implement registration:
  - [ ] Call `api_client.register()`
  - [ ] Auto-login after registration
  - [ ] Navigate to home screen
- [ ] Add token persistence (store locally)
- [ ] Add auto-login on app start if token exists
- [ ] Test authentication flow

**Acceptance Criteria**:
- User can register new account
- User can login with credentials
- Token saved and persisted
- Auto-login works on app restart
- Error messages display correctly

**Estimated Time**: 2-3 hours

---

## Issue #4: Create Home/Dashboard Screen

**Labels**: `frontend`, `ui`, `high-priority`

**Description**:

Create the main dashboard screen with navigation.

**Tasks**:
- [ ] Create `screens/home.py`
- [ ] Design dashboard layout:
  - [ ] Welcome message with username
  - [ ] Current week display
  - [ ] Quick stats (goals completed, journal entries)
  - [ ] Navigation cards:
    - [ ] Weekly Goals
    - [ ] Daily Journal
    - [ ] Weekly Analysis
  - [ ] Settings/logout button
- [ ] Implement navigation to other screens
- [ ] Add pull-to-refresh
- [ ] Test UI and navigation

**Acceptance Criteria**:
- Dashboard displays user info
- Navigation cards work correctly
- Stats display properly
- Clean, intuitive UI

**Estimated Time**: 2-3 hours

---

## Issue #5: Implement Weekly Goals Screen UI

**Labels**: `frontend`, `ui`, `high-priority`

**Description**:

Create the weekly goals management screen.

**Tasks**:
- [ ] Create `screens/goals.py`
- [ ] Design goals screen layout:
  - [ ] List of current week goals
  - [ ] Checkbox to mark complete
  - [ ] Add goal button (FAB)
  - [ ] Goal category display
  - [ ] Empty state message
- [ ] Create add goal dialog:
  - [ ] Text input field
  - [ ] Category selector
  - [ ] Save/Cancel buttons
- [ ] Add swipe to delete
- [ ] Test UI interactions

**Acceptance Criteria**:
- Goals list displays correctly
- Can add new goals
- Can mark goals complete
- Can delete goals
- UI responsive and intuitive

**Estimated Time**: 2-3 hours

---

## Issue #6: Implement Goals API Integration

**Labels**: `frontend`, `api`, `high-priority`

**Description**:

Connect goals screen to backend API.

**Tasks**:
- [ ] Load goals on screen open:
  - [ ] Call `api_client.get_goals()`
  - [ ] Display in list
  - [ ] Show loading indicator
  - [ ] Handle empty state
- [ ] Implement add goal:
  - [ ] Call `api_client.create_goal()`
  - [ ] Refresh list on success
  - [ ] Show error on failure
- [ ] Implement mark complete:
  - [ ] Call `api_client.update_goal()`
  - [ ] Update UI immediately
  - [ ] Show error if fails
- [ ] Implement delete goal:
  - [ ] Call API (to be added)
  - [ ] Remove from list
- [ ] Add error handling
- [ ] Test complete flow

**Acceptance Criteria**:
- Goals load from backend
- Can create new goals
- Can mark complete/incomplete
- Changes persist to backend
- Errors handled gracefully

**Estimated Time**: 2-3 hours

---

## Issue #7: Implement Daily Journal Screen UI

**Labels**: `frontend`, `ui`, `high-priority`

**Description**:

Create the daily journal entry screen.

**Tasks**:
- [ ] Create `screens/journal.py`
- [ ] Design journal screen layout:
  - [ ] Date selector (default to today)
  - [ ] Large text area for journal content
  - [ ] Character/word count
  - [ ] Save button
  - [ ] Language selector (EN/FR)
- [ ] Add date navigation (previous/next day)
- [ ] Show existing entry if date has one
- [ ] Add confirmation before discarding changes
- [ ] Test UI

**Acceptance Criteria**:
- Can select any date
- Text area functional and sized properly
- Can navigate between dates
- Loads existing entries
- Confirmation prevents data loss

**Estimated Time**: 2-3 hours

---

## Issue #8: Implement Journal API Integration

**Labels**: `frontend`, `api`, `high-priority`

**Description**:

Connect journal screen to backend API.

**Tasks**:
- [ ] Load entry when date selected:
  - [ ] Call `api_client.get_journal_by_date()`
  - [ ] Display content if exists
  - [ ] Show empty state if not
- [ ] Implement save:
  - [ ] Call `api_client.create_journal_entry()`
  - [ ] Show success message
  - [ ] Handle errors
- [ ] Add auto-save draft (optional)
- [ ] Test complete flow
- [ ] Handle network errors

**Acceptance Criteria**:
- Entries load from backend
- Can create new entries
- Can edit existing entries
- Changes persist to backend
- Errors handled gracefully

**Estimated Time**: 2-3 hours

---

## Issue #9: Implement Weekly Analysis Screen UI

**Labels**: `frontend`, `ui`, `high-priority`

**Description**:

Create the weekly analysis display screen.

**Tasks**:
- [ ] Create `screens/analysis.py`
- [ ] Design analysis screen layout:
  - [ ] Week selector
  - [ ] "Generate Analysis" button
  - [ ] Loading state during generation
  - [ ] Display analysis sections:
    - [ ] Summary
    - [ ] Goal achievements
    - [ ] Improvement suggestions
    - [ ] Time analysis
    - [ ] Habits analysis
    - [ ] Blind spots
  - [ ] Scrollable content
- [ ] Add empty state (no analysis yet)
- [ ] Add share button (future)
- [ ] Test UI

**Acceptance Criteria**:
- Week selector works correctly
- Analysis displays in organized sections
- Loading state clear to user
- Content readable and well-formatted
- Scrolling smooth

**Estimated Time**: 2-3 hours

---

## Issue #10: Implement Analysis API Integration

**Labels**: `frontend`, `api`, `high-priority`

**Description**:

Connect analysis screen to backend API.

**Tasks**:
- [ ] Load latest analysis on screen open:
  - [ ] Call `api_client.get_latest_analysis()`
  - [ ] Display if exists
  - [ ] Show empty state if not
- [ ] Implement "Generate Analysis":
  - [ ] Show confirmation dialog (API costs money)
  - [ ] Call `api_client.generate_analysis()`
  - [ ] Show progress indicator (may take 10-30 seconds)
  - [ ] Display results when complete
  - [ ] Handle errors (no data, API failure, etc.)
- [ ] Add ability to view past analyses
- [ ] Test complete flow

**Acceptance Criteria**:
- Can generate new analysis
- Loading state shows during generation
- Analysis displays correctly
- Errors handled with clear messages
- Can view past analyses

**Estimated Time**: 2-3 hours

---

## Issue #11: Implement Settings Screen

**Labels**: `frontend`, `ui`, `medium-priority`

**Description**:

Create settings screen for user preferences and account management.

**Tasks**:
- [ ] Create `screens/settings.py`
- [ ] Design settings screen:
  - [ ] User profile section
  - [ ] Theme toggle (Light/Dark)
  - [ ] Language preference (EN/FR)
  - [ ] Notification settings (future)
  - [ ] About section
  - [ ] Logout button
- [ ] Implement logout:
  - [ ] Clear stored token
  - [ ] Navigate to login screen
- [ ] Save preferences locally
- [ ] Test all settings

**Acceptance Criteria**:
- All settings functional
- Preferences persist across app restarts
- Logout works correctly
- Clean, organized UI

**Estimated Time**: 1-2 hours

---

## Issue #12: Add Offline Support and Local Storage

**Labels**: `frontend`, `enhancement`, `medium-priority`

**Description**:

Add basic offline functionality and data caching.

**Tasks**:
- [ ] Create `utils/storage.py` for local data
- [ ] Cache goals locally
- [ ] Cache journal entries locally
- [ ] Implement offline mode detection
- [ ] Queue API calls when offline
- [ ] Sync when connection restored
- [ ] Show offline indicator in UI
- [ ] Test offline behavior

**Acceptance Criteria**:
- App works offline (limited functionality)
- Data cached and available offline
- Changes sync when back online
- User notified of offline status

**Estimated Time**: 3-4 hours

---

## Issue #13: Improve Error Handling and User Feedback

**Labels**: `frontend`, `enhancement`, `medium-priority`

**Description**:

Add better error handling and user feedback throughout the app.

**Tasks**:
- [ ] Create reusable error dialog component
- [ ] Add error handling to all API calls
- [ ] Add success messages for actions
- [ ] Add loading states to all async operations
- [ ] Implement retry logic for failed requests
- [ ] Add helpful error messages (not technical)
- [ ] Test error scenarios

**Acceptance Criteria**:
- All errors handled gracefully
- User always knows what's happening
- Error messages are helpful
- No crashes on API errors

**Estimated Time**: 2-3 hours

---

## Issue #14: Create Reusable UI Components

**Labels**: `frontend`, `refactoring`, `low-priority`

**Description**:

Extract reusable UI components for consistency and maintainability.

**Tasks**:
- [ ] Create `components/goal_card.py`
- [ ] Create `components/journal_entry_card.py`
- [ ] Create `components/analysis_section.py`
- [ ] Create `components/custom_button.py`
- [ ] Create `components/loading_dialog.py`
- [ ] Create `components/error_dialog.py`
- [ ] Update screens to use components
- [ ] Test components

**Acceptance Criteria**:
- Components reusable across screens
- Consistent styling
- Less code duplication
- Easy to maintain

**Estimated Time**: 2-3 hours

---

## Issue #15: Setup Buildozer for Android Build

**Labels**: `mobile`, `build`, `high-priority`

**Description**:

Configure Buildozer to build Android APK.

**Tasks**:
- [ ] Install Buildozer: `pip install buildozer`
- [ ] Initialize: `buildozer init`
- [ ] Configure `buildozer.spec`:
  - [ ] Set app name, package name
  - [ ] Set version
  - [ ] Add permissions (Internet, Network State)
  - [ ] Set requirements
  - [ ] Configure orientation
  - [ ] Set icon
- [ ] Test debug build: `buildozer -v android debug`
- [ ] Document build process in README

**Acceptance Criteria**:
- Buildozer configured correctly
- Debug APK builds successfully
- APK installs on Android device
- App runs on device

**Estimated Time**: 2-3 hours (first build slow)

---

## Issue #16: Test on Android Device

**Labels**: `mobile`, `testing`, `high-priority`

**Description**:

Test complete app functionality on actual Android device.

**Tasks**:
- [ ] Build APK
- [ ] Install on Android device
- [ ] Test authentication flow
- [ ] Test goals management
- [ ] Test journal entries
- [ ] Test analysis generation
- [ ] Test navigation
- [ ] Test on different screen sizes
- [ ] Document issues found
- [ ] Fix critical bugs

**Acceptance Criteria**:
- All core features work on device
- UI displays correctly
- Performance acceptable
- No critical bugs

**Estimated Time**: 2-3 hours

---

## Issue #17: Add Input Validation

**Labels**: `frontend`, `validation`, `medium-priority`

**Description**:

Add comprehensive input validation throughout the app.

**Tasks**:
- [ ] Validate login form inputs
- [ ] Validate registration form
- [ ] Validate goal text (min/max length)
- [ ] Validate journal content
- [ ] Add visual feedback for validation errors
- [ ] Add helpful validation messages
- [ ] Test all validation

**Acceptance Criteria**:
- All inputs validated
- Clear error messages
- Prevents invalid data submission
- Good user experience

**Estimated Time**: 1-2 hours

---

## Issue #18: Improve UI/UX Polish

**Labels**: `frontend`, `ui`, `enhancement`, `low-priority`

**Description**:

Polish UI/UX for better user experience.

**Tasks**:
- [ ] Add animations and transitions
- [ ] Improve color scheme
- [ ] Add app icon and splash screen
- [ ] Improve typography
- [ ] Add empty states illustrations
- [ ] Add success animations
- [ ] Improve button styles
- [ ] Test on multiple devices

**Acceptance Criteria**:
- App looks professional
- Smooth animations
- Consistent design language
- Good accessibility

**Estimated Time**: 3-4 hours

---

## Issue #19: Write User Documentation

**Labels**: `documentation`, `low-priority`

**Description**:

Create user guide and documentation.

**Tasks**:
- [ ] Write user guide in README
- [ ] Create getting started guide
- [ ] Document each screen and feature
- [ ] Add screenshots
- [ ] Add troubleshooting section
- [ ] Add FAQ

**Acceptance Criteria**:
- Complete user documentation
- Screenshots of all screens
- Clear instructions
- Easy to follow

**Estimated Time**: 2-3 hours

---

## Issue #20: Implement Basic Analytics (Optional)

**Labels**: `frontend`, `analytics`, `low-priority`

**Description**:

Add basic usage analytics to understand app usage.

**Tasks**:
- [ ] Choose analytics solution (Firebase, Mixpanel, etc.)
- [ ] Integrate analytics SDK
- [ ] Track key events:
  - [ ] App opens
  - [ ] Goals created
  - [ ] Journal entries saved
  - [ ] Analyses generated
- [ ] Ensure privacy compliance
- [ ] Test analytics

**Acceptance Criteria**:
- Analytics integrated
- Key events tracked
- Privacy respected (no PII)
- Dashboard shows data

**Estimated Time**: 2-3 hours

---

## Milestone: POC Ready

**Target**: Complete issues #1-10 for a working proof of concept
**Estimated Total Time**: 22-28 hours
**Target Date**: 3-4 weeks from start

## Milestone: Production Ready

**Target**: Complete all issues
**Estimated Total Time**: 40-50 hours
**Target Date**: 6-8 weeks from start
