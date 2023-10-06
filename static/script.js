/* Prevent form resubmission upon refresh or back */
if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}
