from utils.dynamic_states import create_dynamic_states_class
from gspread_utils.constants import ABOUT_COMPANY_ID, FEED_BACK_ID, PARTNER_ID
from gspread_utils.text.texts import get_states_count

about_company_states_count = get_states_count(col_id=ABOUT_COMPANY_ID)
feed_back_states_count = get_states_count(col_id=FEED_BACK_ID)
partner_states_count = get_states_count(col_id=PARTNER_ID)
print(about_company_states_count)
print(feed_back_states_count)
print(partner_states_count)


FeedBackDynamicStates = create_dynamic_states_class('FeedBackDynamicStates',
                                                    [f'STATE_{x}' for x in range(1, feed_back_states_count)])
PartnerDynamicStates = create_dynamic_states_class('PartnerDynamicStates',
                                                   [f'STATE_{x}' for x in range(1, partner_states_count)])
