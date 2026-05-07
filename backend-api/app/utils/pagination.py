def paginator(query, skip:int, limit:int):
    total = query.count()
    data = query.offset(skip).limit(limit).all()
    return {
        "total":total,
        "data":data,
        "skip":skip,
        "limit":limit,
        }
