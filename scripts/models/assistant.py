import json, uuid
from .cms_doc import CmsDoc

class Assistant(CmsDoc):
    
    def __init__(self, name=None):
        
        _id = name if name else str(uuid.uuid4())[-25:]
        super().__init__(_id)

        self.name = _id
        self.display_name = _id
        self.locale = 'en_US'
        self.default = {
            "config": {
                "intent.bank_name": "ACMEBank",
                "intent.bot_name": "Kai",
                "intent.ceo_name": "Test",
                "intent.avatar_enabled": True,
                "intent.budget_enabled": True,
                "iapi.disabled_intents": "na",
                "iapi.timezone": "UTC",
                "intent.guai.holdings_api_enabled": "true",
                "intent.kcb_spending_comparison.image_url_base": "https://kaiassets.s3.amazonaws.com/kcb/icons/",
                "intent.kcb_spending_comparison.image_format": "png",
                "iapi.domain_locale": "en_US",
                "intent.kcb_credit_score_monitoring.fi_subscribed_credit_score": "true",
                "intent.kcb_credit_score_monitoring.credit_profile_enabled": "true",
                "intent.kcb_credit_score_range_category_min_max": "excellent=780,850;good=660,779;fair=600,659;poor=500,599;very_poor=300,499",
                "intent.kcb_payment_types_enabled": "local,international,bill",
                "intent.kcb_show_tx.tx_category_enabled": "true",
                "intent.kcb_show_tx.window_size": "month",
                "intent.kcb_withdraw_types_enabled": "atm,credit_card,debit_card",
                "intent.pagesize": "5",
                "intent.convo_starters_enabled": "false",
                "intent.convo_starters.action_priority": "card_activation,new_user,abandoned_intent_finplan,abandoned_intent_generic,high_value_convo",
                "intent.kcb_budget.categories": "food_and_dining,travel,health_and_fitness",
                "intent.kcb_budget.budget_display_type": "text"
            },
            'endpoints': {
                'iapi': {'secret': _id},
                'capi': {'secret': _id},
                'eapi': {'secret': _id}
            }
	    }
        self.targets = [
            {
                'name':'prod',
                'display_name': 'production',
                'primary': True,
                'endpoints':{
                    'capi': {'secret': f'{_id}_prod'},
                    'eapi': {'secret': f'{_id}_prod'}
                }
            },
            {
                'name':'stage',
                'display_name': 'staging',
                'primary': False,
                'endpoints':{
                    'capi': {'secret': f'{_id}_stage'},
                    'eapi': {'secret': f'{_id}_stage'}
                }
            }
        ]
    
    
    def __repr__(self):
        res = json.loads(super().__repr__())
        
        res.update({
            'display_name': self.display_name,
            'locale': self.locale,
            'default': self.default,
            'targets': self.targets  
        })
        
        return str(res)
    
    def get_json(self):
        res = json.loads(super().__repr__())
        
        res.update({
            'display_name': self.display_name,
            'locale': self.locale,
            'default': self.default,
            'targets': self.targets  
        })
        
        return str(json.dumps(res))
    
    def get_id(self):
        return self.name
    
    def get_secret(self, ep, target='default'):
        if target.lower() == 'default':
            return self.default.get('endpoints').get(ep).get('secret')
        elif target:
            return self.default.get('endpoints').get(ep).get('secret')
        elif self.targets:
            for t in self.targets:
                if t.get('name').lower() == target:
                    return t.get('endpoints').get(ep).get('secret')
        return None

    def set_secret(self, secret):
        self.default['endpoints']['iapi']['secret'] = secret
        self.default['endpoints']['capi']['secret'] = secret
        self.default['endpoints']['eapi']['secret'] = secret
