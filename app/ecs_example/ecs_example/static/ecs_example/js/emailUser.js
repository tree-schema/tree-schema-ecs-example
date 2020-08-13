emailUser = function() {

    const ALERT_DANGER = '.alert-danger';
    const ALERT_SUCCESS = '.alert-success';

    async function sendActionToBackend (email, actionId) {
        var action = (actionId == 1) ? 'create-user' : 'send-email';
        const resp = await $.ajax({
            method: 'POST',
            url: '/email_action/',
            data: {
                'action': action,
                'email': email
            },
        });
        return resp;
    };

    function validateEmail(email) {
        // https://stackoverflow.com/questions/46155/how-to-validate-an-email-address-in-javascript?page=1&tab=votes#tab-top
        const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(String(email).toLowerCase());
    }

    function setAlertContentWithResp(resp){
        const alertClass = (resp.success) ? ALERT_SUCCESS : ALERT_DANGER
        $(alertClass).html(resp.message);
        $(alertClass).show();
    }

    async function handleBtnPress(btnId){
        // The input number is embedded in the name of HTML input ID
        // 1 = create new user, 2 = send email
        const inputId = '#' + btnId.replace('btn', 'input');
        const inputNum = btnId.split('-')[1];
        const inputEmail = $(inputId).val();
        if (validateEmail(inputEmail)){
            $(ALERT_DANGER).hide();
            const resp = await sendActionToBackend(inputEmail, inputNum);
            setAlertContentWithResp(resp)
        } 
        else {
            $(ALERT_DANGER).html('Please enter a valid email address.');
            $(ALERT_DANGER).show();
        }
    }
    
    $(document).on('click', 'button', function (e) {
        $('.alert-success').hide();
        const targetId = $(e.target).attr('id');
        handleBtnPress(targetId)
    });
}