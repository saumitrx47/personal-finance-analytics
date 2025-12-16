def add_category_column(df):
        category_rules = {
        "Food": ["swiggy", "zomato", "restaurant", "cafe", "pizza", "burger"],
        "Groceries": ["coles", "woolworths", "grocery", "supermarket"],
        "Transport": ["uber", "didi", "nsw", "transport", "metro"],
        "Shopping": ["amazon", "flipkart", "mall", "nike", "jd sports", "h&m"],
        "Enterntainment": ["strike", "cinema", "bar", "pub", "ekansh", "club", "party"],
        }

        def categorize(description):
                desc = str(description).lower()
                for category, keywords in category_rules.items():
                        if any(keyword in desc for keyword in keywords):
                                return category
                        return "Other"

        df["category"] = df["description"].apply(categorize)
        return df