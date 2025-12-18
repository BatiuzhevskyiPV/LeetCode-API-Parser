HEADERS = {}

QUERY = "\n    query globalRankingPaginated($page: Int) {\n  globalRanking(page: $page) {\n    totalUsers\n    userPerPage\n    totalPages\n    rankingNodes {\n      currentRating\n      currentGlobalRanking\n      dataRegion\n      user {\n        username\n        activeBadge {\n          displayName\n          }\n        profile {\n          userSlug\n          countryCode\n          countryName\n          realName\n        }\n      }\n    }\n  }\n}\n    "
