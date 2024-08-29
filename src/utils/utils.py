import re
from collections import Counter
def get_keywords(string, pattern=None):
    pattern = pattern or r'BE\s+(.*?)\s+BE'  # Default pattern to match anything between BE ... BE
    try:
        regex_pattern = fr'{pattern}'.encode()  # Convert the f-string to bytes
        matches = re.findall(regex_pattern, string.encode())  # Ensure the input string is also bytes
        return [match.decode() for match in matches]  # Decode bytes back to string if needed
    except Exception as e:
        return str(e)
    
def count_keywords(keywords, string):
    count = 0
    for keyword in keywords:
        count += string.count(keyword)
    return count

def recursive_search(keywords, item):
    keyword_set = [str(keyword).lower() for keyword in set(keywords)]
    match = None
    if not isinstance(item,dict):
        item = {"defaultLocal":str(item)}
    if isinstance(item, dict):
        highKey=0
        for key, value in item.items():
            currCount = count_keywords(keyword_set, str(value).lower()) or 0
            if currCount>highKey:
                match=value
                highKey=currCount
    return match if match else None
# Combine all unique words into a single list

async def get_keywordCount(message, dict_obj):
    highestCount = [None, 0]
    
    for key, values in dict_obj.items():
        # Create a regular expression pattern to match any of the keywords as whole words
        pattern = re.compile(r'\b(?:' + '|'.join(map(re.escape, values['uniqueWords'])) + r')\b', re.IGNORECASE)
        
        # Find all keyword matches in the string
        matches = pattern.findall(message)
        
        # Count the occurrences of each keyword
        keyword_count = sum(Counter(matches).values())
        
        # Check if the current keyword count is higher than the previous highest count
        if keyword_count > highestCount[1]:
            highestCount = [key, keyword_count]
    
    return highestCount[0]



