hpp_functions = '''
#ifndef __mg_functions_h__
#define __mg_functions_h__

#include <map>
#include <vector>

template <class T=int, class P>
bool in_map(const T& key, const std::map<T, P>& map)
{
	return map.count(key) > 0;
}

template <class T, class P>
bool in_map(int element, const std::map<T, P>& map)
{
	return map.count(element) > 0;
}

template <class T>
bool in_list(const T& item, const std::vector<T>& list)
{
    return std::find(list.begin(), list.end(), item) != list.end();
}

template <class T>
void list_push(std::vector<T>& list, const T& t)
{
    list.push_back(t);
}

template <class T>
int list_size(const std::vector<T>& vector)
{
    return static_cast<int>(vector.size());
}

template <class T, class P>
int map_size(const std::map<T, P>& map)
{
    return static_cast<int>(map.size());
}

#endif
'''
cpp_functions = '''
'''
