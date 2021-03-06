##############################################
#  IMPORT STATEMENTS
##############################################

# >>>> Native <<<<
from typing import Dict, List, Any, Tuple, Hashable, Iterable, Union
from collections import defaultdict

# >>>> Local <<<<
from dummy_models import TypeDummyModel, BeliefStateDummyModel, PolicyDummyModel, SysDummyModel

##############################################
#                  CONFIG Dict
#
# The config dict describes all the data fields.
# This is also the place to specify models and label types.
#
# Available label types:
#
#     => "multilabel_classification" :: displays as checkboxes in front end
#
#     => "multilabel_classification_string" :: displays as a checkbox and text input for string value. Used for
#                                              slot-value pairs.
#
#     => "string" :: displays underneath the user utterance (indicated by label_type of "data")
#
#############################################

##############################################
#  CODE
##############################################


class Configuration(object):
    """
    class responsible for configuration and valid annotation structure
    """


    configDict = {

        "usr": {
            "description" : "Person",
            "label_type"  : "data",  # This type, "data", acts the same as "string" but will always be displayed first in UI
            "required"    : True
        },


        "1A_-_Cause": {

            "description" : "Type of cause underlying the emotion. Select at least 1.",
            "label_type"  : "multilabel_classification",
            "required"    : False,
            "labels"      : [
                "Agree with action",
                "Agree with opinion",
                "Disagree with action",
                "Disagree with opinion",
                "Conflict",
                "Harmony",
                "Goal achieved",
                "Goal not achieved",
                "Empathy",
                "Apathy",
                "Subject of deceit",
                "subject of persuation",
                "Past experience",
                "Curiosity",
                "Personal opinion",
                "None",
                "Other (elaborate in 1B below)"
            ]

        },

        "1B_-_Other_Cause_Detail": {

            "description" : "Optionally provide more information about the cause",
            "label_type"  : "multilabel_classification_string",
            "required"    : False,
            "labels"      : [
                "other_detail"
            ]
        },
        
        "2_-_Needs_Fulfillment": {

            "description" : "Indicate fulfillment of Marslow need",
            "label_type"  : "multilabel_classification",
            "required"    : False,
            "labels"      : [
                "Physiological - fulfilled",
                "Physiological - NOT fulfilled",
                "Safety - fulfilled",
                "Safety - NOT fulfilled",
                "Social - fulfilled",
                "Social - NOT fulfilled",
                "Esteem - fulfilled",
                "Esteem - NOT fulfilled",
                "Self-actualisation - fulfilled",
                "Self-actualisation - NOT fulfilled",
                "N/A",
            ]
        },

        "3_-_Problematic": {

            "description" : "Describe any issue with the current turn",
            "label_type"  : "multilabel_classification_string",
            "required"    : False,
            "labels"      : [
                "problem_detail"
            ]
        },

        "context": {
            "description" : "Relevant Cause Context",
            "label_type"  : "string",
            "required"    : False
        },

        

    }

    @staticmethod
    def validate_dialogue(dialogue: List[Dict[str, Any]]) -> Union[str, List[Dict]]:
        """
        validates the dialogue and makes sure it conforms to the configDict
        """

        for i, turn in enumerate(dialogue):

            for labelName, info in Configuration.configDict.items():

                try:
                    turn[labelName]
                except KeyError:
                    if info["required"]:
                        return "ERROR1: Label \'{}\' is listed as \"required\" in the " \
                               "config.py file, but is missing from the provided " \
                               "dialogue in turn {}.".format(labelName, i)

                if info["required"] and not turn[labelName]:
                    return "ERROR2: Required label, \'{}\', does not have a value " \
                           "provided in the dialogue in turn {}".format(labelName, i)

                if "multilabel_classification" == info["label_type"]:

                    providedLabels = turn[labelName]

                    if not all(x in info["labels"] for x in providedLabels):
                        return "ERROR3: One of the provided labels in the list: " \
                               "\'{}\' is not in allowed list according to " \
                               "config.py in turn {}".format(providedLabels, i)

        return dialogue



    @staticmethod
    def create_annotation_dict():
        """
        Generates a dictionary mapping label names to a dictionary of their description, label types
        and, if applicable, the possible values the label can take.
        """
        out = {}

        for key,value in Configuration.configDict.items():

            temp = list(value["labels"]) if value.get("labels") else ""

            out[key] = {
                "label_type": value["label_type"],
                "labels": temp,
                "info": value["description"]
            }

        return out


    @staticmethod
    def create_empty_turn():
        """
        creates an empty turn based on the configuration dictionary
        """
        out = {}

        for key,value in Configuration.configDict.items():

            labelType = value["label_type"]

            if labelType == "data":
                out[key] = query

            elif labelType == "multilabel_classification" or \
                 labelType == "multilabel_classification_string":

                out[key] = []

            elif labelType == "string":

                out[key] = ""

            else:

                raise ValueError("The label type, {}, is not supported"
                                 .format(labelType))

        return out








##############################################
#  MAIN
##############################################


# EOF
