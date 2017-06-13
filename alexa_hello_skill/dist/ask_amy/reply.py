import logging
from ask_amy.object_dictionary import ObjectDictionary

logger = logging.getLogger()


class Reply(ObjectDictionary):
    def __init__(self, card_dict=None):
        super().__init__(card_dict)

    @classmethod
    def constr(cls, response, session_attributes=None):
        logger.debug("**************** entering Reply.constr")
        reply = {'version': '1.0'}
        if session_attributes is not None:
            reply['sessionAttributes'] = session_attributes
        reply['response'] = response.json()
        return cls(reply)

    @staticmethod
    def build(intent_dict, session=None):
        logger.debug("**************** entering Reply.build")
        prompt = None
        reprompt = None
        card = None
        logger.debug("intent_dict={}".format(intent_dict))

        if 'speech_out_text' in intent_dict:
            logger.debug("speech_out_text={}".format(intent_dict['speech_out_text']))
            prompt = Prompt.text(intent_dict['speech_out_text'], session)
        if 're_prompt_text' in intent_dict:
            logger.debug("re_prompt_text={}".format(intent_dict['re_prompt_text']))
            reprompt = Prompt.text(intent_dict['re_prompt_text'], session)
        if 'speech_out_ssml' in intent_dict:
            prompt = Prompt.ssml(intent_dict['speech_out_ssml'], session)
        if 're_prompt_ssml' in intent_dict:
            reprompt = Prompt.ssml(intent_dict['re_prompt_ssml'], session)
        if 'should_end_session' in intent_dict:
            should_end_session = intent_dict['should_end_session']
        else:
            should_end_session = True
        if 'card_title' in intent_dict:
            logger.debug("card_title={}".format(intent_dict['card_title']))
            card = Card.simple(intent_dict['card_title'], intent_dict['speech_out_text'], session)
        # todo build out proper card in reply
        if 'card' in intent_dict:
            pass

        response = Response.constr(prompt, reprompt, card, should_end_session)
        reply = Reply.constr(response, session.attributes())
        return reply.json()


class Response(ObjectDictionary):
    def __init__(self, card_dict=None):
        super().__init__(card_dict)

    @classmethod
    def constr(cls, out_speech, reprompt=None, card=None, should_end_session=True):
        logger.debug("**************** entering Response.constr")
        response = {}
        if out_speech is not None:
            response['outputSpeech'] = out_speech.json()
        if reprompt is not None:
            output_speech = {'outputSpeech': reprompt.json()}
            response['reprompt'] = output_speech
        if card is not None:
            response['card'] = card.json()
        if should_end_session is not None:
            response['shouldEndSession'] = should_end_session
        return cls(response)


class OutText(ObjectDictionary):
    def __init__(self, card_dict=None):
        super().__init__(card_dict)

    @staticmethod
    def concat_text_if_list(text_obj):
        logger.debug("**************** entering OutText.concat_text_if_list")
        text_str = ''
        if type(text_obj) is str:
            text_str = text_obj
        elif type(text_obj) is list:
            for text_line in text_obj:
                text_str += text_line
        return text_str

    @staticmethod
    def map_vales_to_names(text, session):
        logger.debug("**************** entering OutText.map_vales_to_names")
        if text is None: return text
        out_list = []
        indx = 0
        len_text = len(text)
        done = False
        while not done:
            start_token_index = text.find("{")
            if start_token_index == -1:
                out_list.append(text)
                done = True
            else:
                end_token_index = text.find("}")
                fragment = text[indx:start_token_index]
                token = text[start_token_index + 1:end_token_index]
                text = text[end_token_index + 1:len(text)]
                if fragment != '':
                    out_list.append(fragment)
                out_list.append(OutText.process_token(token, session))
                if text.find("{") == -1:
                    if text != '':
                        out_list.append(text)
                    done = True
        print(out_list)
        return "".join(out_list)

    @staticmethod
    def process_token(token, session):
        logger.debug("**************** entering OutText.process_token")
        value = session.get_attribute([token])
        if value is None:
            value = ''
        return str(value)


class Prompt(OutText):
    def __init__(self, card_dict=None):
        super().__init__(card_dict)

    @classmethod
    def ssml(cls, ssml, session=None):
        logger.debug("**************** entering Prompt.ssml")
        ssml = Prompt.concat_text_if_list(ssml)
        if session is not None:
            ssml = Prompt.map_vales_to_names(ssml, session)
        prompt = {'type': 'SSML', 'ssml': "<speak>{}</speak>".format(ssml)}
        return cls(prompt)

    @classmethod
    def text(cls, text, session=None):
        logger.debug("**************** entering Prompt.text")
        text = Prompt.concat_text_if_list(text)
        if session is not None:
            text = Prompt.map_vales_to_names(text, session)
        prompt = {'type': 'PlainText', 'text': text}
        return cls(prompt)


class Card(OutText):
    def __init__(self, card_dict=None):
        super().__init__(card_dict)

    @classmethod
    def simple(cls, title, content, session=None):
        logger.debug("**************** entering Card.simple")
        content = Card.concat_text_if_list(content)
        if session is not None:
            content = Card.map_vales_to_names(content, session)
        card = {'type': 'Simple', 'title': title, 'content': content}
        return cls(card)

    @classmethod
    def standard(cls, title, content, small_image_url, large_image_url, session=None):
        logger.debug("**************** entering Card.standard")
        content = Card.concat_text_if_list(content)
        if session is not None:
            content = Card.map_vales_to_names(content, session)
        card = {'type': 'Standard', 'title': title, 'text': content}
        image = {}
        card['image'] = image
        image['smallImageUrl'] = small_image_url
        image['largeImageUrl'] = large_image_url
        return cls(card)


