#include <list>
#include <vector>

#include <tick/traits.h>
#include <tick/trait_check.h>

int 
main(int, char *[])
{
  static_assert(!tick::is_associative_container<std::vector<int>>(), "Not a associative container");
  static_assert(!tick::is_associative_container<std::list<int>>(), "Not a associative container");

  return 0;
}
