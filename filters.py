import re

# filters = [filter_by_subs]

# def meets_criteria(channel_list):
    
#     is_us()
    
#     return True


# def check_channels():
#     filtered_channels = []
#     for channel in channels:
#         if meets_criteria(channel) == True:
#             filtered_channels.append(channel)
#     return filtered_channels

# def is_us():



def filter_by_subs(channel_list, min_subscriber_count, max_subscriber_count):    
    filtered_channels = []

    for channel in channel_list:
        if int(min_subscriber_count) < int(channel["subscriber_count"]) < int(max_subscriber_count):
            filtered_channels.append(channel)

    channel_with_emails = add_emails(filtered_channels)

    return channel_with_emails

def add_emails(filtered_channels):
    
    for channel in filtered_channels:
        emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", channel["description"])
        channel["email"] = emails

    return(filtered_channels)



    


