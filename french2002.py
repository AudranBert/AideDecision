import re
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, FrozenSet

parse_name = re.compile(r"^# ALTERNATIVE NAME (\d+): (.*)$")
parse_choices = re.compile(r"^\{?([\d,]*)\}?,\{?([\d,]*)\}?$")

CandidateId = int
        

@dataclass
class VotingInfo:
    candidate_names: Dict[CandidateId, str]
    profiles: Dict[FrozenSet[int], int]

    @classmethod
    def default(cls) -> "VotingInfo":
        return VotingInfo(
            candidate_names={},
            profiles=defaultdict(int)
        )


    @classmethod
    def from_file(cls, fname: str) -> "VotingInfo":
        info = VotingInfo.default()

        with open(fname) as f:
            lines = f.read().split("\n")

        for line in lines:
            name_match = parse_name.findall(line)
            if len(name_match) != 0:
                candidate_id, candidate_name = name_match[0]
                candidate_id = int(candidate_id)
                info.candidate_names[candidate_id] = candidate_name

            # comment/data description
            if line.startswith("#"):
                continue

            line = line.strip()

            # empty line
            if len(line) == 0:
                continue

            count, _, choices_raw = line.partition(": ")
            count = int(count)
            
            try:
                pref_raw, _nonpref_raw = parse_choices.findall(choices_raw)[0]
            except IndexError:
                print(f"Failed to parse line '{line}'! Skipping.\n")
                continue
            
            def parse_list(raw):
                return frozenset({
                    int(e) for e in raw.split(",")
                    if len(e) != 0
                })
            
            # print(pref_raw, " - ", nonpref_raw)

            key = parse_list(pref_raw)
            info.profiles[key] += count
        
        return info


    @classmethod
    def from_files(cls, fnames: List[str]) -> "VotingInfo":
        info = VotingInfo.default()

        for fname in fnames:
            info.merge_with(VotingInfo.from_file(fname))

        return info


    def candidate_id_set(self):
        return set(self.candidate_names.keys())


    def merge_with(self, other: "VotingInfo"):
        self.candidate_names.update(other.candidate_names)

        for profile, count in other.profiles.items():
            self.profiles[profile] += count


    def format_candidate_ids(self, candidate_ids):
        return ", ".join(self.candidate_names[i] for i in candidate_ids)


    def format_profile(self, pref, nonpref, count):
        return f"{count}: + {self.format_candidate_ids(pref)}"


def pref_frequencies(info: VotingInfo):
    in_pref = defaultdict(int)

    for prefs, count in info.profiles.items():
        for pref in prefs:
            in_pref[pref] += count

    return in_pref


def print_sorted_freq(freqs, info: VotingInfo):
    sorted_freqs = sorted(freqs.items(), key=lambda kv: -kv[1])

    for candidate_id, freq in sorted_freqs:
        print(f"{info.candidate_names[candidate_id]: <15}: {freq}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("paths", type=str, nargs="+")

    args = parser.parse_args()

    info = VotingInfo.from_files(args.paths)
    
    in_pref = pref_frequencies(info)
    
    print_sorted_freq(in_pref, info)