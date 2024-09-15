class in_utils():
    def restriction_ordering(sites, features):
        def get_distance(site):
            min_dist = float('inf')
            site_loc = site['location']

            for feat in features:
                if feat['start'] <= site_loc <= feat['end']:
                    return -1
                dist_to_start = abs(site_loc - feat['start'])
                dist_to_end = abs(site_loc - feat['end'])
                min_dist = min(min_dist, dist_to_start, dist_to_end)

            return min_dist

        sites.sort(reverse=True, key=get_distance)

        return sites

    