import logging
import json
import os
import sys
import importlib

logger = logging.getLogger()


class SkillFactory(object):
    SKILL_CONFIG = 'skill_configuration.json'

    def __init__(self):
        pass

    @staticmethod
    def build(config_file_name=None):
        logger.warn("**************** entering SkillFactory.build")
        if config_file_name is None:
            config_file_name = SkillFactory.SKILL_CONFIG
        config_dict = SkillFactory.__load(config_file_name)

        # todo add exception management
        skill_dict = config_dict['Skill']
        skill_class_name = skill_dict['className']
        SkillFactory.set_logging_level(skill_dict)
        skill_obj = SkillFactory.__import_class_from_str(skill_class_name)
        dialog_dict = config_dict['Dialog']
        return skill_obj(dialog_dict)

    @staticmethod
    def set_logging_level(skill_dict):
        logger.debug("**************** entering SkillFactory.set_logging_level")
        logging_levels = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "WARN": logging.WARN,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL
        }
        try:
            logging_level = skill_dict['loggingLevel']
            logging_level = logging_level.upper()
            if logging_level == 'NONE':
                root_logger = logging.getLogger()
                root_logger.disabled = True
            else:
                set_level = logging_levels[logging_level]
                logger.setLevel(set_level)
        except KeyError as e:

            pass

    @staticmethod
    def load_configuartion(config_name, config_file_name=None):
        logger.debug("**************** entering SkillFactory.load_configuartion")
        if config_file_name is None:
            config_file_name = SkillFactory.SKILL_CONFIG
        config_dict = SkillFactory.__load(config_file_name)
        obj__config_dict = config_dict[config_name]
        return obj__config_dict

    @staticmethod
    def __load(file_name):
        logger.debug("**************** entering SkillFactory.__load")
        dialog_dict = None
        not_found = True
        path = sys.path
        path.insert(0, "./")
        for x in path:
            resource = os.path.join(x, file_name)
            if os.path.isfile(resource):
                file_ptr_r = open(resource, 'r')
                dialog_dict = json.load(file_ptr_r)
                file_ptr_r.close()
                not_found = False
                break

        if not_found:
            logger.critical("Error in SkillFactory.__load seaching for file {} ".format(file_name))
            raise FileNotFoundError

        return dialog_dict

    @staticmethod
    def __import_class_from_str(dotted_path):
        logger.debug("**************** entering SkillFactory.__import_class_from_str")
        module = None
        class_name = None
        try:
            module_path, class_name = dotted_path.rsplit('.', 1)
            module = importlib.import_module(module_path)
        except ValueError:
            logger.critical("Error SkillFactory.__import_class_from_str")
            # todo Add proper exception management

        try:
            return getattr(module, class_name)
        except AttributeError as err:
            logger.critical("Error in SkillFactory.__import_class_from_str path {} err={}".format(dotted_path, err))
