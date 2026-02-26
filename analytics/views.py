from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from config.utils.mongo import collection


class TopRoutesView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        pipeline = [
            {
                "$group": {
                    "_id": {
                        "source": "$source",
                        "destination": "$destination"
                    },
                    "count": {"$sum": 1}
                }
            },
            {"$sort": {"count": -1}},
            {"$limit": 5}
        ]

        results = list(collection.aggregate(pipeline))

        formatted = [
            {
                "source": r["_id"]["source"],
                "destination": r["_id"]["destination"],
                "search_count": r["count"]
            }
            for r in results
        ]

        return Response(formatted)