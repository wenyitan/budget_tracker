def get_aggregate_for_breakdown_by_month_and_person(month, person):
    return [
            {
                "$match": {
                    "$or": [
                        { "person": person },
                        { "person": {"$ne": person}, "shared": True}
                    ]
                }
            },
            {
                "$match": {"date": {"$regex": f"{month}$"}}
            },
            {
                "$addFields": {
                    "adjusted_amount": {
                        "$cond": [
                            "$shared",
                            { "$divide": ["$amount", 2] },
                            "$amount"
                        ]
                    },
                    "shared_amount": {
                        "$cond": [
                            "$shared",
                            { "$divide": ["$amount", 2] },
                            0
                        ]
                    }
                }
            },
            {
                "$group": {
                    "_id": "$category",
                    "total": {
                        "$sum": "$adjusted_amount"
                    },
                    "shared_total": {
                        "$sum": "$shared_amount"
                    }
                }
            },
            {
                "$facet": {
                    "breakdown": [],
                    "total": [
                        {
                            "$group": {
                                "_id": None,
                                "total": {
                                    "$sum": "$total"
                                },
                                "shared_total": {
                                    "$sum": "$shared_total"
                                }
                            }
                        }
                    ]
                }
            },
            {
                "$project": {
                    "breakdown": 1,
                    "total": {
                        "$arrayElemAt": ["$total.total", 0]
                    },
                    "shared_total": {
                        "$arrayElemAt": ["$total.shared_total", 0]
                    },
                    "unshared_total": {
                        "$subtract": [
                            { "$arrayElemAt": ["$total.total", 0] },
                            { "$arrayElemAt": ["$total.shared_total", 0] }
                        ]
                    }
                }
            } 
        ]