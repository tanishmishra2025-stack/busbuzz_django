function addLoginType() {
    if ($('#loginUsername').val().trim() === '') {
        $('#loginUsername').focus()
        showErrorToast(' Please enter login username ')
        return false;
    }
    else if ($('#loginPassword').val().trim() === '') {
        $('#loginPassword').focus()
        showErrorToast(' Please enter login password')
        return false;
    }

    else {
        return true;
    }
}