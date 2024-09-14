class in_utils():
    def restriction_ordering(sites, features):
        def get_distance(site):
            # which has the greatest min dist
            min_dist = 1000000
        
            site = site['location']

            for feat in features:
                if abs(site - feat['start']) < min_dist:
                    min_dist = abs(site - feat['start'])
                elif abs(site - feat['end']) < min_dist:
                    min_dist = abs(site - feat['end'])

            return min_dist
                          
        sites.sort(key=get_distance)

        return sites

    