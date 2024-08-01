#include <string>
#include <utility>
#include <iostream>
#include <vector>

#include "shield_absl/strings/str_cat.h"
#include "shield_absl/strings/str_split.h"
#include "shield_absl/container/flat_hash_map.h"
#include "shield_absl/container/flat_hash_set.h"
#include "shield_absl/numeric/int128.h"
#include "shield_absl/time/time.h"
#include "shield_absl/types/variant.h"

int main()
{
    shield_absl::flat_hash_set<std::string> set1;
    shield_absl::flat_hash_map<int, std::string> map1;
    shield_absl::flat_hash_set<std::string> set2 = {
        {"huey"},
        {"dewey"},
        {"louie"},
    };
    shield_absl::flat_hash_map<int, std::string> map2 = {
        {1, "huey"},
        {2, "dewey"},
        {3, "louie"},
    };
    shield_absl::flat_hash_set<std::string> set3(set2);
    shield_absl::flat_hash_map<int, std::string> map3(map2);

    shield_absl::flat_hash_set<std::string> set4;
    set4 = set3;
    shield_absl::flat_hash_map<int, std::string> map4;
    map4 = map3;

    shield_absl::flat_hash_set<std::string> set5(std::move(set4));
    shield_absl::flat_hash_map<int, std::string> map5(std::move(map4));
    shield_absl::flat_hash_set<std::string> set6;
    set6 = std::move(set5);
    shield_absl::flat_hash_map<int, std::string> map6;
    map6 = std::move(map5);

    const shield_absl::uint128 big = shield_absl::Uint128Max();
    std::cout << shield_absl::StrCat("Arg ", "foo", "\n");
    std::vector<std::string> v = shield_absl::StrSplit("a,b,,c", ',');

    shield_absl::Time t1 = shield_absl::Now();
    shield_absl::Time t2 = shield_absl::Time();
    shield_absl::Time t3 = shield_absl::UnixEpoch();

    shield_absl::variant<int> v1 = shield_absl::variant<int>();
    shield_absl::bad_variant_access e1;

    std::string const year = shield_absl::FormatTime("%Y", shield_absl::Now(), shield_absl::UTCTimeZone());
    std::cout << "year " << year << std::endl;
}
