def _build_request_envelope(request):
    return {
        "version": "1.0",
        "session": {
            "new": True,
            "sessionId": "amzn1.echo-api.session.test",
            "application": {"applicationId": "amzn1.ask.skill.test"},
            "user": {"userId": "amzn1.ask.account.test"},
        },
        "context": {
            "System": {
                "application": {"applicationId": "amzn1.ask.skill.test"},
                "user": {"userId": "amzn1.ask.account.test"},
                "device": {"deviceId": "amzn1.ask.device.test", "supportedInterfaces": {}},
                "apiEndpoint": "https://api.amazonalexa.com",
            }
        },
        "request": request,
    }


def test_launch_request_returns_welcome_prompt(lambda_handler_module):
    event = _build_request_envelope(
        {
            "type": "LaunchRequest",
            "requestId": "amzn1.echo-api.request.test-launch",
            "timestamp": "2026-08-22T00:00:00Z",
            "locale": "ja-JP",
        }
    )

    response = lambda_handler_module.lambda_handler(event, None)

    assert "室内環境" in response["response"]["outputSpeech"]["ssml"]
    assert response["response"]["shouldEndSession"] is False


def test_env_monitor_intent_returns_sensor_values(lambda_handler_module):
    event = _build_request_envelope(
        {
            "type": "IntentRequest",
            "requestId": "amzn1.echo-api.request.test-env-monitor",
            "timestamp": "2026-08-22T00:00:00Z",
            "locale": "ja-JP",
            "intent": {"name": "EnvMonitorIntent", "confirmationStatus": "NONE"},
        }
    )

    response = lambda_handler_module.lambda_handler(event, None)

    speech = response["response"]["outputSpeech"]["ssml"]
    assert "25.3" in speech
    assert "48.2" in speech
    assert "1012.5" in speech


def test_cancel_intent_returns_goodbye(lambda_handler_module):
    event = _build_request_envelope(
        {
            "type": "IntentRequest",
            "requestId": "amzn1.echo-api.request.test-cancel",
            "timestamp": "2026-08-22T00:00:00Z",
            "locale": "ja-JP",
            "intent": {"name": "AMAZON.CancelIntent", "confirmationStatus": "NONE"},
        }
    )

    response = lambda_handler_module.lambda_handler(event, None)

    assert "さようなら" in response["response"]["outputSpeech"]["ssml"]
    # shouldEndSession defaults to True and is omitted from the serialized response in that case.
    assert response["response"].get("shouldEndSession", True) is True
