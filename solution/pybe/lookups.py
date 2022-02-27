import logging

logger = logging.getLogger(__name__)

def apply_lookups(provider,json):
    ret_json = json
    # is_new
    if provider == 1:
        if json.get("is_new") == "New":
            ret_json["is_new"] = True
        elif json.get("is_new") == "Used":
            ret_json["is_new"] = False
        else:
            logger.warning("Invalid value for is_new")
            return

    elif provider == 2:
        ret_json["is_new"] = True if json.get("is_new") == "N" else False
    
    else:
        logger.warning("Invalid provider")
        return

    # msrp and invoice
    if ret_json.get("is_new") == False:
        # msrp
        ret_json["dealer_msrp"] = ret_json.get("dealer_list_price")
        # invoice
        ret_json["dealer_invoice"] = ret_json.get("dealer_list_price")

    # certified
    if json.get("dealer_certified") == "Yes":
        ret_json["dealer_certified"] = True
    else:
        ret_json["dealer_certified"] = False

    
    
    
    return ret_json