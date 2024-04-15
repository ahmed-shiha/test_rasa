# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

import requests
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from typing import Any, Dict, List, Text
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.events import EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict


class CallClassifierAPIAction(Action):
    def name(self) -> Text:
        return "action_call_classifier_api"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        feeling_1_value = tracker.get_slot('feeling_1')
        feeling_2_value = tracker.get_slot('feeling_2')

        # Concatenate the slot values
        combined_feelings = f"{feeling_1_value} {feeling_2_value}"

        # Send the concatenated text to the API
        response = requests.post('http://35.207.141.136:8080/predict', json={'text': combined_feelings})
        print(response)
        # Process the API response
        if response.status_code == 200:
            output = response.json()
            sentiment_1 = output.get('sentiment_1')
            sentiment_2 = output.get('sentiment_2')
            print(sentiment_1)
            print(output)
            # Update the slots with the obtained sentiments
            return [
                SlotSet("sentiment_1", sentiment_1),
                SlotSet("sentiment_2", sentiment_2)
            ]

        return []
    

class CallClassifierAPIAction_2(Action):
    def name(self) -> Text:
        return "action_call_classifier_api_2"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        feeling_1_value = tracker.get_slot('feeling_1')
        print(feeling_1_value)
        feeling_2_value = tracker.get_slot('feeling_2')

        # Concatenate the slot values
        combined_feelings = f"{feeling_1_value} {feeling_2_value}"

        # Send the concatenated text to the API
        print('run classifier')
        response = requests.post('http://35.207.141.136:8080/predict', json={'text': combined_feelings})
        print(response)
        # Process the API response
        if response.status_code == 200:
            output = response.json()
            sentiment_1 = output.get('sentiment_1')
            sentiment_2 = output.get('sentiment_2')
            print(sentiment_1)
            print(output)
            # Update the slots with the obtained sentiments
            return [
                SlotSet("sentiment_1", sentiment_1),
                SlotSet("sentiment_2", sentiment_2)
            ]

        return []
    
class SuicideTest(Action):
    def name(self) -> Text:
        return "suicide_test"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Questions to ask the user
        questions = [
            "هل تمنيت لو كنت ميتا أو تمنيت أن تنام ولا تستيقظ؟", #death_wish
            "هل كان لديك فعلياً أي أفكار حول قتل نفسك؟" #actual_kill_thought
        ]

        # Provide buttons for the user to select
        buttons = [{"title": "نعم", "payload": "/affirm"}, {"title": "لا", "payload": "/deny"}]

        suicide_quest = ""

        for i, question in enumerate(questions):
            dispatcher.utter_message(text=question, buttons=buttons)
            user_response = tracker.latest_message.get("text")

            # Concatenate user's responses into one string
            suicide_quest += f" {user_response}" if user_response else ""

            # If the user answered "نعم" to the second question, ask additional questions
            if i == 1 and "نعم" in user_response:
                additional_questions = [
                    "هل كنت تفكر في كيفية القيام بذلك؟", # thinking_how_to_do
                    "هل راودتك تلك الأفكار الانتحارية وكان لديك بعض النية لتنفيذها؟", # suicidal_thoughts_with_intention
                    "هل بدأت في التخطيط أو العمل على تفاصيل للتخلص من حياتك؟ هل تنوي تنفيذ هذه الخطة؟", # planning_details_get_rid_of_life
                    "هل فعلت أي شيء أو بدأت في فعل أي شيء لإنهاء حياتك أو تستعد لفعل ذلك؟" # started_doing_anything_end_life 
                ]

                for additional_question in additional_questions:
                    dispatcher.utter_message(text=additional_question, buttons=buttons)
                    user_response_additional = tracker.latest_message.get("text")

                    # Concatenate additional responses into the same string
                    suicide_quest += f" {user_response_additional}" if user_response_additional else ""

        # Update the 'suicide_quest' slot with the concatenated responses
        tracker.slots["suicide_quest"] = suicide_quest.strip()

        return []
    
class ValidateFeelingForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_feeling_form"

    def validate_feeling_1(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `feeling_1` value."""

        if len(slot_value.split()) < 3:
            dispatcher.utter_message(text=f"أرجو أن تقوم بشرح حالتك بوصف مفصل حتى نتمكن من مساعدتك")
            return {"feeling_1": None}
        # dispatcher.utter_message(text=f"")
        return {"feeling_1": slot_value}

    def validate_feeling_2(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `feeling_2` value."""

        # if slot_value not in ALLOWED_PIZZA_TYPES:
        #     dispatcher.utter_message(
        #         text=f"I don't recognize that pizza. We serve {'/'.join(ALLOWED_PIZZA_TYPES)}."
        #     )
        #     return {"pizza_type": None}
        # dispatcher.utter_message(text=f"OK! You want to have a {slot_value} pizza.")
        return {"feeling_2": slot_value}

# class AskForVegetarianAction(Action):
#     def name(self) -> Text:
#         return "action_ask_vegetarian"

#     def run(
#         self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
#     ) -> List[EventType]:
#         dispatcher.utter_message(
#             text="Would you like to order a vegetarian pizza?",
#             buttons=[
#                 {"title": "yes", "payload": "/affirm"},
#                 {"title": "no", "payload": "/deny"},
#             ],
#         )
#         return []

class ValidateSuicideForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_suicide_form"

    def validate_death_wish(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `death_wish` value."""

        if not slot_value:
            # If user chooses death_wish as false, set other slots to false
            return {
                "death_wish": slot_value,
                "thinking_how_to_do": False,
                "suicidal_thoughts_with_intention": False,
                "planning_details_get_rid_of_life": False
            }

        return {"death_wish": slot_value}

    def validate_actual_kill_thought(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `actual_kill_thought` value."""



    def validate_thinking_how_to_do(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `thinking_how_to_do` value."""


    
    def validate_suicidal_thoughts_with_intention(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `suicidal_thoughts_with_intention` value."""


    
    def validate_planning_details_get_rid_of_life(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `planning_details_get_rid_of_life` value."""

    
    def validate_started_doing_anything_end_life(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `started_doing_anything_end_life` value."""

class PostSuicideFormAction(Action):
    def name(self) -> Text:
        return "action_post_suicide_form"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict
    ) -> List[Dict[Text, Any]]:
        actual_kill_thought = tracker.get_slot("actual_kill_thought")
        thinking_how_to_do = tracker.get_slot("thinking_how_to_do")
        suicidal_thoughts_with_intention = tracker.get_slot("suicidal_thoughts_with_intention")
        planning_details_get_rid_of_life = tracker.get_slot("planning_details_get_rid_of_life")
        started_doing_anything_end_life = tracker.get_slot("started_doing_anything_end_life")


        if suicidal_thoughts_with_intention or planning_details_get_rid_of_life or started_doing_anything_end_life:
            dispatcher.utter_message("You need immediate help. Please seek assistance.")
        
        elif actual_kill_thought or thinking_how_to_do:
            dispatcher.utter_message("You need behavioral healthcare for further evaluation.")

        return []
    
# class AskTimeSpentIntrusiveThoughts(Action):
#     def name(self) -> Text:
#         return "action_ask_time_spent_intrusive_thoughts"

#     def run(
#         self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
#     ) -> List[EventType]:
#         dispatcher.utter_message(
#             text=f"ما مقدار الوقت الذي تستغرقه الأفكار الوسواسية ?",
#             buttons = [
#     {"title": "لا شيء", "payload": "/optionA"},
#     {"title": "أقل من ساعة في اليوم ، أو تتكرر أحيانا )بمعدل 8 مرات فأقل يوميا(", "payload": "optionB"},
#     {"title": "من ساعة إلى 3 ساعات في اليوم، أو تتكرر كثيرا )أكثر من 8 مرات في اليوم لكن معظم ساعات اليوم خالية من الأفكار الوسواسية(.", "payload": "optionC"},
#     {"title": "من 3 إلى 8 ساعات في اليوم ، أو تحدث كثيرا جدا )تحدث أكثر من 8 مرات في اليوم وفي معظم ساعات اليوم(", "payload": "optionD"},
#     {"title": "أكثر من 8 ساعات في اليوم ، أو تحدث بشكل دائم )أكثر من تحملها ونادرا ما ماتمر ساعة بدون", "payload": "optionE"}
# ]
# ,
#             )
       
#         return []


class ActionGetRandomArticle(Action):
    def name(self) -> Text:
        return "action_get_random_article"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Make the API request
        api_url = "http://192.168.1.15:8000/api/random_article?category_name=الإنتحار"
        response = requests.get(api_url)

        # Parse the response
        if response.status_code == 200:
            data = response.json()
            article = data.get("message", {})
            title = article.get("title", "")
            author = article.get("author", "")
            body = article.get("body", "")

            # Formulate the message to send to the user
            message = f"Title: {title}\nAuthor: {author}\n\n{body}"

            # Send the message to the user
            dispatcher.utter_message(text=message)
        else:
            dispatcher.utter_message(text="Failed to fetch the article. Please try again later.")

        return []
    

from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.forms import FormValidationAction
from typing import Any, Dict, List, Text

class ValidateOcdForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_ocd_form"

    def validate_time_spent_intrusive_thoughts(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate `time_spent_intrusive_thoughts` value."""
        return self.validate_numeric_slot("time_spent_intrusive_thoughts", tracker)

    def validate_conflict_with_activities(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate `conflict_with_activities` value."""
        return self.validate_numeric_slot("conflict_with_activities", tracker)

    def validate_anxiety_level(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate `anxiety_level` value."""
        return self.validate_numeric_slot("anxiety_level", tracker)

    def validate_effort_in_resisting_thoughts(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate `effort_in_resisting_thoughts` value."""
        return self.validate_numeric_slot("effort_in_resisting_thoughts", tracker)

    def validate_control_over_intrusive_thoughts(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate `control_over_intrusive_thoughts` value."""
        return self.validate_numeric_slot("control_over_intrusive_thoughts", tracker)

    def validate_time_spent_compulsive_behaviors(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate `time_spent_compulsive_behaviors` value."""
        return self.validate_numeric_slot("time_spent_compulsive_behaviors", tracker)

    def validate_conflict_with_activities_compulsive_behaviors(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate `conflict_with_activities_compulsive_behaviors` value."""
        return self.validate_numeric_slot("conflict_with_activities_compulsive_behaviors", tracker)

    def validate_anxiety_level_compulsive_behaviors(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate `anxiety_level_compulsive_behaviors` value."""
        return self.validate_numeric_slot("anxiety_level_compulsive_behaviors", tracker)

    def validate_effort_in_resisting_behaviors(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate `effort_in_resisting_behaviors` value."""
        return self.validate_numeric_slot("effort_in_resisting_behaviors", tracker)

    def validate_control_over_compulsive_behaviors(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate `control_over_compulsive_behaviors` value."""
        return self.validate_numeric_slot("control_over_compulsive_behaviors", tracker)

    def validate_numeric_slot(
            self,
            slot_name: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
    ) -> Dict[Text, Any]:
        """Generic method to validate numeric slots."""
        intent = tracker.get_intent_of_latest_message()
        numeric_values_mapping = {
            "/optionA": 0,
            "/optionB": 1,
            "/optionC": 2,
            "/optionD": 3,
            "/optionE": 4,
        }

        if intent in numeric_values_mapping:
            return {slot_name: numeric_values_mapping[intent]}

        dispatcher.utter_message(text="I didn't get that.")
        return {slot_name: None}
    

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import List, Dict, Any, Text

class PostOcdFormAction(Action):
    def name(self) -> Text:
        return "action_post_ocd_form"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # Retrieve all slot values from the form
        time_spent_intrusive_thoughts = tracker.get_slot("time_spent_intrusive_thoughts")
        conflict_with_activities = tracker.get_slot("conflict_with_activities")
        anxiety_level = tracker.get_slot("anxiety_level")
        effort_in_resisting_thoughts = tracker.get_slot("effort_in_resisting_thoughts")
        control_over_intrusive_thoughts = tracker.get_slot("control_over_intrusive_thoughts")
        time_spent_compulsive_behaviors = tracker.get_slot("time_spent_compulsive_behaviors")
        conflict_with_activities_compulsive_behaviors = tracker.get_slot("conflict_with_activities_compulsive_behaviors")
        anxiety_level_compulsive_behaviors = tracker.get_slot("anxiety_level_compulsive_behaviors")
        effort_in_resisting_behaviors = tracker.get_slot("effort_in_resisting_behaviors")
        control_over_compulsive_behaviors = tracker.get_slot("control_over_compulsive_behaviors")

        # Mapping of options to numeric values
        numeric_values_mapping = {
            "/optionA": 0,
            "/optionB": 1,
            "/optionC": 2,
            "/optionD": 3,
            "/optionE": 4,
        }

        # Calculate the total score based on slot values and mapping
        total_score = (
            numeric_values_mapping.get(time_spent_intrusive_thoughts, 0) +
            numeric_values_mapping.get(conflict_with_activities, 0) +
            numeric_values_mapping.get(anxiety_level, 0) +
            numeric_values_mapping.get(effort_in_resisting_thoughts, 0) +
            numeric_values_mapping.get(control_over_intrusive_thoughts, 0) +
            numeric_values_mapping.get(time_spent_compulsive_behaviors, 0) +
            numeric_values_mapping.get(conflict_with_activities_compulsive_behaviors, 0) +
            numeric_values_mapping.get(anxiety_level_compulsive_behaviors, 0) +
            numeric_values_mapping.get(effort_in_resisting_behaviors, 0) +
            numeric_values_mapping.get(control_over_compulsive_behaviors, 0)
        )

        dispatcher.utter_message(f"The total score is: {total_score}")

        return []

####__new__##

from typing import List, Dict, Any, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# class ActionProvideGadResult(Action):
#     def name(self) -> Text:
#         return "action_gad_result"

#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         # Mapping of scores for each question
#         score_mapping = {
#             "/optionA": 0,
#             "/optionB": 1,
#             "/optionC": 2,
#             "/optionD": 3,
#             "/optionE": 4,
#         }

#         # Extract slot values from the tracker
#         feeling_nervous = tracker.get_slot("feeling_nervous")
#         unable_to_control_worrying = tracker.get_slot("unable_to_control_worrying")
#         worrying_too_much = tracker.get_slot("worrying_too_much")
#         trouble_relaxing = tracker.get_slot("trouble_relaxing")
#         restlessness = tracker.get_slot("restlessness")
#         easily_irritable = tracker.get_slot("easily_irritable")
#         feeling_afraid = tracker.get_slot("feeling_afraid")

#         # Calculate the GAD-7 score
#         gad_7_score = (
#             score_mapping.get(feeling_nervous, 0)
#             + score_mapping.get(unable_to_control_worrying, 0)
#             + score_mapping.get(worrying_too_much, 0)
#             + score_mapping.get(trouble_relaxing, 0)
#             + score_mapping.get(restlessness, 0)
#             + score_mapping.get(easily_irritable, 0)
#             + score_mapping.get(feeling_afraid, 0)
#         )

#         # Provide the GAD-7 score to the user politely in Arabic
#         dispatcher.utter_message(text=f"تشير نتيجة الاختبار إلى {self.get_severity_level(gad_7_score)}")

#         return []

#     def get_severity_level(self, score: int) -> Text:
#         if score >= 15:
#             return "قلق شديد، من المهم البحث عن دعم ومساعدة من محترف صحي."
#         elif score >= 10:
#             return "قلق متوسط، قد تحتاج إلى اهتمام إضافي وتقييم."
#         elif score >= 5:
#             return " تشير نتيجتك إلى وجود بعض مظاهر القلق الخفيفة . ."
#         else:
#             return "قلق بسيط ، مما يعني أن مستوى القلق لديك طبيعي."

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

escore_mapping = {
    "/optionA": 0,
    "/optionB": 1,
    "/optionC": 2,
    "/optionD": 3,
    "/optionE": 4,
}

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

escore_mapping = {
    "/optionA": 0,
    "/optionB": 1,
    "/optionC": 2,
    "/optionD": 3,
    "/optionE": 4,
}

class ActionGadFormResult(Action):
    def name(self) -> Text:
        return "action_gad_form_result"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        gad_questions = [
            "feeling_nervous",
            "unable_to_control_worrying",
            "worrying_too_much",
            "trouble_relaxing",
            "restlessness",
            "easily_irritable",
            "feeling_afraid",
        ]

        gad_score = 0

        for question in gad_questions:
            slot_key = f"{question}"
            if tracker.get_slot(slot_key) in escore_mapping:
                gad_score += escore_mapping[tracker.get_slot(slot_key)]

        response_message = (
            f"نتيجة الاختبار = {gad_score}.\n"
            f"استناداً إلى نتيجتك، فالأعراض التي تعاني منها تقع في فئة {self.get_severity_level(gad_score)}.\n"
        )

        if gad_score >= 5:
            response_message += (
                "تذكر أن هذه النتائج تعطينا لمحة عامة ولا تغني عن زيارة مختص ومن المهم أن تطلب الدعم من متخصص ، لا يجب أن تمر بهذا وحدك.\n"
                ". إليك تفصيلا حول ما تعنيه النتائج عموما:\n"
                "المجموع.          التفسير\n"
                "0-4.                قلق منخفض\n"
                "5-9.               قلق متوسط\n"
                "10-14              قلق متوسط الى شديد\n"
                "15-21              قلق شديد\n"
            )
        else:
            response_message += (
                "تذكر أن هذه النتائج تعطينا لمحة عامة ولا تغني عن زيارة مختص.\n"
                "إليك تفصيلا حول ما تعنيه النتائج عموما:\n"
                "المجموع.          التفسير\n"
                "0-4.                قلق منخفض\n"
                "5-9.               قلق متوسط\n"
                "10-14              قلق متوسط الى شديد\n"
                "15-21              قلق شديد\n"
            )

        dispatcher.utter_message(text=response_message)

        return []

    def get_severity_level(self, score: int) -> Text:
        if score >= 15:
            return "قلق شديد"
        elif score >= 10:
            return "قلق متوسط الى شديد"
        elif score >= 5:
            return "قلق متوسط"
        else:
            return "قلق منخفض"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

escore_mapping = {
    "/optionA": 0,
    "/optionB": 1,
    "/optionC": 2,
    "/optionD": 3,
}

class ActionPhq9FormResult(Action):
    def name(self) -> Text:
        return "action_phq9_form_result"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        phq9_questions = [
            "little_interest",
            "feeling_down",
            "trouble_sleeping",
            "feeling_tired",
            "poor_appetite",
            "feeling_bad_about_self",
            "trouble_concentrating",
            "moving_slow_or_fast",
            "thoughts_of_self_harm",
        ]

        phq9_score = 0

        for question in phq9_questions:
            slot_key = f"{question}"
            if tracker.get_slot(slot_key) in escore_mapping:
                phq9_score += escore_mapping[tracker.get_slot(slot_key)]

        response_message = (
            f"نتيجة الاختبار = {phq9_score}.\n"
            f"استناداً إلى نتيجتك، فالأعراض التي تعاني منها تقع في فئة {self.get_severity_level(phq9_score)}.\n"
        )

        if phq9_score >= 20:
            response_message += "0-4 عدم وجود أعراض للاكتئاب\n"
        elif phq9_score >= 15:
            response_message += "20-27 اكتئاب شديد\n"
        elif phq9_score >= 10:
            response_message += "15-19 اكتئاب متوسط إلى شديد\n"
        elif phq9_score >= 5:
            response_message += "10-14 اكتئاب متوسط\n"
        else:
            response_message += "5-9 اكتئاب خفيف\n"

        dispatcher.utter_message(text=response_message)

        return []

    def get_severity_level(self, score: int) -> Text:
        if score >= 20:
            return "اكتئاب شديد"
        elif score >= 15:
            return "اكتئاب متوسط إلى شديد"
        elif score >= 10:
            return "اكتئاب متوسط"
        elif score >= 5:
            return "اكتئاب خفيف"
        else:
            return "عدم وجود أعراض للاكتئاب"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

escore_mapping = {
    "/optionA": 0,
    "/optionB": 1,
    "/optionC": 2,
    "/optionD": 3,
}

class ActionOcdFormResult(Action):
    def name(self) -> Text:
        return "action_ocd_form_result"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        ocd_questions = [
            "time_spent_intrusive_thoughts",
            "conflict_with_activities",
            "anxiety_level",
            "effort_in_resisting_thoughts",
            "control_over_intrusive_thoughts",
            "time_spent_compulsive_behaviors",
            "conflict_with_activities_compulsive_behaviors",
            "anxiety_level_compulsive_behaviors",
            "effort_in_resisting_behaviors",
            "control_over_compulsive_behaviors",
        ]

        ocd_score = 0

        for question in ocd_questions:
            slot_key = f"{question}"
            if tracker.get_slot(slot_key) in escore_mapping:
                ocd_score += escore_mapping[tracker.get_slot(slot_key)]

        response_message = (
            f"نتيجة الاختبار = {ocd_score}.\n"
            f"استناداً إلى نتيجتك، فالأعراض التي تعاني منها تقع في فئة {self.get_severity_level(ocd_score)}.\n"
        )

        dispatcher.utter_message(text=response_message)

        return []

    def get_severity_level(self, score: int) -> Text:
        if score >= 32:
            return "أعراض الوسواس القهري متطرفة"
        elif score >= 24:
            return "أعراض الوسواس القهري شديدة"
        elif score >= 16:
            return "أعراض الوسواس القهري متوسطة"
        elif score >= 8:
            return "أعراض الوساس القهري خفيفة"
        else:
            return "لا توجد أعراض (طبيعي)"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionSuicideTestResult(Action):
    def name(self) -> Text:
        return "action_suicide_test_result"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        death_wish = tracker.get_slot("death_wish_slot")
        actual_kill_thought = tracker.get_slot("actual_kill_thought_slot")
        thinking_how_to_do = tracker.get_slot("thinking_how_to_do_slot")
        suicidal_thoughts_with_intention = tracker.get_slot("suicidal_thoughts_with_intention_slot")
        planning_details_get_rid_of_life = tracker.get_slot("planning_details_get_rid_of_life_slot")
        started_doing_anything_end_life = tracker.get_slot("started_doing_anything_end_life_slot")

        if actual_kill_thought or thinking_how_to_do or suicidal_thoughts_with_intention:
            dispatcher.utter_message(
                text="طبقا لنتائج الاختبار فأنت تعاني من بعض الميول الخطيرة بفضل بشدة أن تتحدث مع محترف في الصحة النفسية او طبيب لمناقشة حالتك وتقديم الدعم المناسب."
                     "لا تقلق فستجد لديهم الخبرة اللازمة لتقديم تقييم شامل وخطة علاجية مناسبة."
                     "\n\nأريد أن أؤكد لك أنك لست وحدك في هذا وأننا دائما بجانبك"
            )
        else:
            dispatcher.utter_message(
                text="طبقا لنتائج الاختبار فأنت لا تعاني من أي ميول انتحارية،"
                     "مع ذلك، إن كان لديك بعض الصعوبات الخفيفة التي ترغب في مناقشتها مع متخصص في الدعم النفسي فقد يكون ذلك مفيدا لك."
            )

        return []

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

class ActionShowVideo(Action):
    def name(self) -> Text:
        return "action_show_video"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get the sentiment_1 slot value from the tracker
        sentiment_1 = tracker.get_slot("sentiment_1")

        # Capitalize the sentiment_1 value
        sentiment_1_capitalized = sentiment_1.capitalize()

        # Construct the API URL with the capitalized sentiment_1 value
        api_url = f"https://backend.ihayanow.com/api/youtube_by_category?name={sentiment_1_capitalized}"

        # Make a request to the API
        response = requests.get(api_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the API response
            video_data = response.json()

            # Check if there is at least one video in the response
            if video_data:
                # Get the first video details
                video_details = video_data[0]

                # Extract relevant information
                video_title = video_details["knowledgebase"]["title"]
                video_url = video_details["url"]

                # Construct the message to be sent to the user
                message = (
                    f"يمكنك مشاهدة الفيديو التالي:\n"
                    f"[{video_title}]({video_url})"
                )

                # Send the message to the user
                dispatcher.utter_message(text=message)
            else:
                dispatcher.utter_message(text="للأسف، لا يوجد فيديوهات متاحة في الوقت الحالي.")
        else:
            dispatcher.utter_message(text="عذراً، حدثت مشكلة أثناء جلب الفيديو. يرجى المحاولة مرة أخرى لاحقًا.")

        return []

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

class ActionShowTips(Action):
    def name(self) -> Text:
        return "action_show_tips"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get the sentiment_1 slot value from the tracker
        sentiment_1 = tracker.get_slot("sentiment_1")

        # Capitalize the sentiment_1 value
        sentiment_1_capitalized = sentiment_1.capitalize()

        # Construct the API URL with the capitalized sentiment_1 value
        api_url = f"https://backend.ihayanow.com/api/tips_by_category?name={sentiment_1_capitalized}"

        # Make a request to the API
        response = requests.get(api_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the API response
            tips_data = response.json()

            # Check if there is at least one tip in the response
            if tips_data:
                # Get the first tip details
                tip_details = tips_data[0]

                # Extract relevant information
                tip_title = tip_details["knowledgebase"]["title"]
                tip_author = tip_details["knowledgebase"]["author"]
                tip_body = tip_details["knowledgebase"]["body"]

                # Construct the message to be sent to the user
                message = (
                    f"نصيحة من {tip_author} بعنوان '{tip_title}':\n"
                    f"{tip_body}"
                )

                # Send the message to the user
                dispatcher.utter_message(text=message)
            else:
                dispatcher.utter_message(text="للأسف، لا يوجد نصائح متاحة في الوقت الحالي.")
        else:
            dispatcher.utter_message(text="عذراً، حدثت مشكلة أثناء جلب النصائح. يرجى المحاولة مرة أخرى لاحقًا.")

        return []

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

class ActionShowArticle(Action):
    def name(self) -> Text:
        return "action_show_article"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get the sentiment_1 slot value from the tracker
        sentiment_1 = tracker.get_slot("sentiment_1")

        # Capitalize the sentiment_1 value
        sentiment_1_capitalized = sentiment_1.capitalize()

        # Construct the API URL with the capitalized sentiment_1 value
        api_url = f"https://backend.ihayanow.com/api/article_by_category?name={sentiment_1_capitalized}"

        # Make a request to the API
        response = requests.get(api_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the API response
            article_data = response.json()

            # Check if there is at least one article in the response
            if article_data:
                article = article_data[0]['knowledgebase']
                article_title = article['title']
                doctor_name = article['author']
                article_link = article_data[0]['url']
                # Get the first article details
                # article_details = article_data[0]

                # # Extract relevant information
                # article_title = article_details["knowledgebase"]["title"]
                # article_link = article_details["knowledgebase"]["url"]

                # Construct the message to be sent to the user
                message = (
                    f"يمكنك قراءة المقال التالي للدكتور {doctor_name}:\n"
                    f"[{article_title}]({article_link})"
                )

                # Send the message to the user
                dispatcher.utter_message(text=message)
            else:
                dispatcher.utter_message(text="للأسف، لا يوجد مقالات متاحة في الوقت الحالي.")
        else:
            dispatcher.utter_message(text="عذراً، حدثت مشكلة أثناء جلب المقال. يرجى المحاولة مرة أخرى لاحقًا.")

        return []

from typing import Any, Dict, List, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

class ActionShowDoctor(Action):
    def name(self) -> Text:
        return "action_show_doctor"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get values of slots from the tracker
        city_name = tracker.get_slot("city_name")
        session_type = tracker.get_slot("session_type")
        max_price_online = tracker.get_slot("maxPriceOnline")
        min_price_online = tracker.get_slot("minPriceOnline")

        # Define mappings for each slot
        city_name_mapping = {
            "/optionA": "مدينة نصر",
            "/optionB": "أكتوبر",
            "/optionC": "بولاق",
            "/optionD": "الفردوس",
            "/optionE": "أخرى",
        }

        session_type_mapping = {
            "/optionA": "Online",
            "/optionB": "Onsite",
        }

        max_price_online_mapping = {
            "/optionA": '300',
            "/optionB": '400',
            "/optionC": '500',
            "/optionD": '1000',
            "/optionE": 'أخرى',
        }

        min_price_online_mapping = {
            "/optionA": '200',
            "/optionB": '300',
            "/optionC": '400',
            "/optionD": '500',
            "/optionE": 'أخرى',
        }

        # Map slot values to their corresponding titles
        city_name_title = city_name_mapping.get(city_name, city_name)
        session_type_title = session_type_mapping.get(session_type, session_type)
        max_price_online_title = max_price_online_mapping.get(max_price_online, max_price_online)
        min_price_online_title = min_price_online_mapping.get(min_price_online, min_price_online)

        # Construct the API URL with the mapped slot values
        api_url = f"https://backend.ihayanow.com/api/random_doctor?city_name={city_name_title}&session_type={session_type_title}&maxPriceOnline={max_price_online_title}&minPriceOnline={min_price_online_title}"

        # Make a request to the API
        response = requests.get(api_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the API response
            doctor_data = response.json()

            # Check if there is at least one doctor in the response
            if doctor_data["message"]:
                doctor_name = doctor_data[0]["doctor_name"]
                arabic_name = doctor_data[0]["profile"]["arabic_name"]
                doctor_url = doctor_data[0]["url"]
                message = (
                f"النتائج التالية تتوافق مع اختياراتك:\n"
                )
                message_2 = (
                f"الدكتور: {arabic_name}"
                )

                # Send the message to the user
                dispatcher.utter_message(text=message)
                dispatcher.utter_message(text=message_2)

                # Construct the second message with a clickable hyperlink
                hyperlink_message = (
                    f"[يمكنك فتح صفحة الدكتور والحجز من هنا]({doctor_url})"
                )

                # Send the clickable hyperlink message to the user
                dispatcher.utter_message(text=hyperlink_message)
                return []
            else:
                dispatcher.utter_message(text="عذراً، لا يوجد أطباء متاحين في الوقت الحالي.")
        else:
            dispatcher.utter_message(text="عذراً، حدثت مشكلة أثناء جلب قائمة الأطباء. يرجى المحاولة مرة أخرى لاحقًا.")

        return []

# class ActionProvidePHQ9Result(Action):
#     def name(self) -> Text:
#         return "action_provide_phq9_result"

#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         # Mapping of scores for each question
#         score_mapping = {
#             "/optionA": 0,
#             "/optionB": 1,
#             "/optionC": 2,
#             "/optionD": 3,
#             "/optionE": 4,
#         }

#         # Extract slot values from the tracker
#         little_interest = tracker.get_slot("little_interest")
#         feeling_down = tracker.get_slot("feeling_down")
#         trouble_sleeping = tracker.get_slot("trouble_sleeping")
#         feeling_tired = tracker.get_slot("feeling_tired")
#         poor_appetite = tracker.get_slot("poor_appetite")
#         feeling_bad_about_self = tracker.get_slot("feeling_bad_about_self")
#         trouble_concentrating = tracker.get_slot("trouble_concentrating")
#         moving_slow_or_fast = tracker.get_slot("moving_slow_or_fast")
#         thoughts_of_self_harm = tracker.get_slot("thoughts_of_self_harm")

#         # Calculate the PHQ-9 score
#         phq9_score = (
#             score_mapping.get(little_interest, 0)
#             + score_mapping.get(feeling_down, 0)
#             + score_mapping.get(trouble_sleeping, 0)
#             + score_mapping.get(feeling_tired, 0)
#             + score_mapping.get(poor_appetite, 0)
#             + score_mapping.get(feeling_bad_about_self, 0)
#             + score_mapping.get(trouble_concentrating, 0)
#             + score_mapping.get(moving_slow_or_fast, 0)
#             + score_mapping.get(thoughts_of_self_harm, 0)
#         )

#         # Set the PHQ-9 score as a slot
#         dispatcher.utter_slot("phq9_score", phq9_score)

#         # Provide the PHQ-9 score to the user
#         severity_level = self.get_severity_level(phq9_score)
#         dispatcher.utter_message(text=f"تشير نتيجتك إلى {severity_level}")

#         return []

#     def get_severity_level(self, score: int) -> Text:
#         if score >= 20:
#             return "الاكتئاب الشديد، من المهم البحث عن دعم ومساعدة من محترف صحي."
#         elif score >= 15:
#             return "الاكتئاب المتوسط ​​، قد تحتاج إلى اهتمام إضافي وتقييم."
#         elif score >= 10:
#             return "الاكتئاب الخفيف، وهو أمر يمكن التعامل معه بشكل جيد."
#         else:
#             return "تشير نتيجتك إلى افتقاد لأعراض الاكتئاب البارزة."
