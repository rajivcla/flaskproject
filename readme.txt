To improve the performance of this app given several hundred thousand search strings, 
I would need to optimize the vsn_data from a list to another data structure.  Assuming that the first 4
letters are normally distributed among the set of all VSN search strings and all search strings do not have wild cards
in the first 4 locations, a factor of 26^4 improvement by indexing is available either in a database or dictionary.
Additionally, there are many duplicate search strings which can be removed if the other column data is unimportant.

This app uses flask_restplus to handle the API routes.
