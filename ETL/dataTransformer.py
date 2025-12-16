def add_category_column(df):
        category_rules = {
        "Food": ["swiggy", "zomato", "restaurant", "cafe", "pizza", "burger"],
        "Groceries": ["coles", "woolworths", "grocery", "supermarket"],
        "Transport": ["uber", "didi", "nsw", "transport", "metro"],
        "Shopping": ["amazon", "flipkart", "mall", "nike", "jd sports", "h&m"],
        "Enterntainment": ["bowling", "cinema", "bar", "pub", "ekansh", "club", "party"],
        "Income": ["salary", "bonus", "refund", "interest"],
        "Utilities": ["electricity", "water", "internet", "phone", "gas"],
        "Healthcare": ["pharmacy", "hospital", "clinic", "doctor", "medical"],
        "Education": ["school", "college", "university", "tuition", "course"],
        "Travel": ["flight", "hotel", "airbnb", "booking", "travel"],
        "Bills": ["rent", "mortgage", "insurance", "subscription", "netflix"],
        }

        def categorize(description):
                desc = str(description).lower()
                for category, keywords in category_rules.items():
                        if any(keyword in desc for keyword in keywords):
                                return category
                return "Other"

        df["category"] = df["description"].apply(categorize)
        return df