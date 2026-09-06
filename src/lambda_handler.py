import json
import logging
import os

import ask_sdk_core.utils as ask_utils
from ask_sdk_core.dispatch_components import AbstractExceptionHandler, AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_model import Response
from ask_sdk_model.interfaces.alexa.presentation.apl import RenderDocumentDirective

from .env_monitor import EnvMonitor

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

env_monitor = EnvMonitor()

APL_DOCUMENT_PATH = os.path.join(os.path.dirname(__file__), "env_monitor_document.json")


def load_apl_document(file_path):
    """Load the APL json document at the path into a dict object."""
    with open(file_path, encoding="utf-8") as json_file:
        return json.load(json_file)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        logger.info("In LaunchRequestHandler")

        speak_output = "ようこそ。「室内環境」と言ってみて。"

        return handler_input.response_builder.speak(speak_output).ask(speak_output).response


class EnvMonitorIntentHandler(AbstractRequestHandler):
    """Handler for Env Monitor Intent."""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.is_intent_name("EnvMonitorIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        logger.info("In EnvMonitorIntentHandler")

        snapshot = env_monitor.get_snapshot()
        env_temperature = round(snapshot["temperature"], 1)
        env_humidity = round(snapshot["humidity"], 1)
        env_pressure = round(snapshot["pressure"], 1)

        speak_output = f"室内環境は、温度：{env_temperature}℃、湿度：{env_humidity}%、気圧：{env_pressure}hPaです。"

        if ask_utils.get_supported_interfaces(handler_input).alexa_presentation_apl is not None:
            handler_input.response_builder.add_directive(
                RenderDocumentDirective(
                    token="EnvMonitorDocumentToken",
                    document=load_apl_document(APL_DOCUMENT_PATH),
                    datasources={
                        "EnvMonitorDataSource": {
                            "envTemperature": env_temperature,
                            "envHumidity": env_humidity,
                            "envPressure": env_pressure,
                        }
                    },
                )
            )

        return handler_input.response_builder.speak(speak_output).response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        logger.info("In HelpIntentHandler")

        speak_output = "室内環境を聞きたい時は「室内環境」、終わりたい時は「おしまい」と言ってみて。"

        return handler_input.response_builder.speak(speak_output).ask(speak_output).response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or ask_utils.is_intent_name(
            "AMAZON.StopIntent"
        )(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        logger.info("In CancelOrStopIntentHandler")

        speak_output = "さようなら。"

        return handler_input.response_builder.speak(speak_output).response


class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for Fallback Intent."""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        logger.info("In FallbackIntentHandler")

        speak_output = "その質問にはお答えできませんが、室内環境を聞きたい時は「室内環境」と言ってみて。"

        return handler_input.response_builder.speak(speak_output).ask(speak_output).response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        logger.info("In SessionEndedRequestHandler")
        logger.info("Session ended reason: %s", handler_input.request_envelope.request.reason)
        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = f"You just triggered {intent_name}."

        return handler_input.response_builder.speak(speak_output).response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """

    def can_handle(self, handler_input: HandlerInput, exception: Exception) -> bool:
        return True

    def handle(self, handler_input: HandlerInput, exception: Exception) -> Response:
        logger.info("In CatchAllExceptionHandler")
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return handler_input.response_builder.speak(speak_output).ask(speak_output).response


# The SkillBuilder object acts as the entry point for the skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors are included below.
# The order matters - they're processed top to bottom.
sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(EnvMonitorIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
# Keep IntentReflectorHandler last so it doesn't override custom intent handlers.
sb.add_request_handler(IntentReflectorHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
