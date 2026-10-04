#!/usr/bin/env python3
"""Reproduce the finite address-105 case using Python's standard library."""
from pathlib import Path
from decimal import Decimal, getcontext
import argparse
import csv
import io
import json

getcontext().prec = 40
ROOT = Path(__file__).resolve().parent


def csv_bytes(rows):
    buf = io.StringIO(newline="")
    writer = csv.DictWriter(buf, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buf.getvalue().encode("utf-8")


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def number(value):
    return format(value, "f") if isinstance(value, Decimal) else value


def assemble(address, primes, descending=False):
    ordered = list(reversed(primes)) if descending else list(primes)
    remainder = address
    counts = {p: 0 for p in primes}
    trace, instances = [], []
    cycle = 0
    while remainder >= min(primes):
        cycle += 1
        for rank, prime in enumerate(ordered, 1):
            before = remainder
            accepted = int(prime <= before)
            instance_id = ""
            if accepted:
                counts[prime] += 1
                remainder -= prime
                instance_id = f"p{prime}_occurrence{counts[prime]}"
                instances.append({"selection_index": len(instances)+1,
                                  "prime_label": prime,
                                  "occurrence_index": counts[prime],
                                  "instance_id": instance_id})
            trace.append({"cycle": cycle, "visit_rank": rank,
                          "prime_label": prime, "accepted": accepted,
                          "remaining_before": before,
                          "remaining_after": remainder,
                          "consumed_address_after": address-remainder,
                          "instance_id": instance_id})
    return counts, remainder, trace, instances


def generate(config):
    primes = config["prime_pool"]
    neutron_labels = set(config["neutron_component_labels"])
    masses = {k: Decimal(v) for k, v in config["rest_energies_MeV"].items()}
    mn, mp, me = masses["neutron"], masses["proton"], masses["electron"]
    release = mn-mp-me
    outputs = {}
    for case, descending in (("small_first", False), ("large_first", True)):
        outputs[case] = assemble(config["address"], primes, descending)
    common_baryons = max(sum(v[0].values()) for v in outputs.values())
    common_residue = max(v[1] for v in outputs.values())
    source_energy = mn*(common_baryons+common_residue)
    trace_rows, instance_rows, component_rows, ledger_rows = [], [], [], []
    checks = {}
    def check(name, condition):
        checks[name] = bool(condition)
        if not condition:
            raise AssertionError(name)
    for case, (counts, remainder, trace, instances) in outputs.items():
        for row in trace:
            trace_rows.append({"case": case, **row})
        for row in instances:
            kind = "neutron" if row["prime_label"] in neutron_labels else "daughter_bundle"
            instance_rows.append({"case": case, **row, "readout": kind})
        for prime in primes:
            component_rows.append({"case": case, "prime_label": prime,
                                   "multiplicity": counts[prime],
                                   "address_contribution": prime*counts[prime],
                                   "readout": "neutron" if prime in neutron_labels else "daughter_bundle"})
        neutrons = sum(counts[p] for p in neutron_labels if p in counts)
        daughters = sum(counts.values())-neutrons
        active_baryons = neutrons+daughters
        reserve_baryons = common_baryons-active_baryons
        rest_energy = neutrons*mn+daughters*(mp+me)
        nonrest_energy = daughters*release
        reserve_energy = reserve_baryons*mn
        residue_energy = remainder*mn
        buffer_energy = (common_residue-remainder)*mn
        accounted_energy = rest_energy+nonrest_energy+reserve_energy+residue_energy+buffer_energy
        charge = daughters-daughters
        lepton_number = daughters-daughters
        row = {"case": case, "address_integer": config["address"],
               "summed_prime_labels": sum(p*n for p,n in counts.items()),
               "residual_address_integer": remainder,
               "active_components": active_baryons,
               "active_neutrons": neutrons, "active_protons": daughters,
               "active_electrons": daughters, "active_electron_antineutrinos": daughters,
               "reserve_baryons": reserve_baryons, "total_baryons": common_baryons,
               "total_charge_e": charge, "total_lepton_number": lepton_number,
               "source_energy_MeV": source_energy,
               "active_rest_energy_MeV": rest_energy,
               "daughter_nonrest_budget_MeV": nonrest_energy,
               "reserve_energy_MeV": reserve_energy,
               "address_residue_energy_MeV": residue_energy,
               "neutral_buffer_energy_MeV": buffer_energy,
               "accounted_energy_MeV": accounted_energy,
               "energy_closure_residual_MeV": accounted_energy-source_energy}
        ledger_rows.append({k:number(v) for k,v in row.items()})
        check(case+"_address_identity", sum(p*n for p,n in counts.items())+remainder==config["address"])
        check(case+"_trace_preserves_each_step", all(r["remaining_before"]-r["remaining_after"]==r["accepted"]*r["prime_label"] for r in trace))
        check(case+"_trace_matches_instances", sum(r["accepted"] for r in trace)==len(instances)==active_baryons)
        check(case+"_nonnegative_reserve", reserve_baryons>=0)
        check(case+"_baryon_closure", active_baryons+reserve_baryons==common_baryons)
        check(case+"_charge_closure", charge==0)
        check(case+"_lepton_closure", lepton_number==0)
        check(case+"_energy_closure", accounted_energy==source_energy)
        check(case+"_neutron_origin_retained", len([r for r in instances if r["prime_label"] in neutron_labels])==neutrons)
    small, large = outputs["small_first"], outputs["large_first"]
    check("small_expected_sequence", [r["prime_label"] for r in small[3]]==[2,3,5,7,11,13,17,19,23,2,3])
    check("large_expected_sequence", [r["prime_label"] for r in large[3]]==[47,43,13,2])
    check("common_baryon_budget_is_11", common_baryons==11)
    check("both_address_residues_are_zero", small[1]==large[1]==0)
    check("release_budget_positive", release>0)
    # Apply a recomputed balance to deliberately altered copies of actual ledgers.
    def balances_close(row):
        baryons = int(row["active_neutrons"])+int(row["active_protons"])+int(row["reserve_baryons"])
        charge = int(row["active_protons"])-int(row["active_electrons"])
        lepton = int(row["active_electrons"])-int(row["active_electron_antineutrinos"])
        energy = sum(Decimal(row[key]) for key in (
            "active_rest_energy_MeV", "daughter_nonrest_budget_MeV",
            "reserve_energy_MeV", "address_residue_energy_MeV", "neutral_buffer_energy_MeV"))
        return baryons==int(row["total_baryons"]) and charge==0 and lepton==0 and energy==Decimal(row["source_energy_MeV"])
    incomplete = {**ledger_rows[1], "reserve_baryons":0, "reserve_energy_MeV":"0"}
    check("reject_large_case_missing_reserve", not balances_close(incomplete))
    incomplete = {**ledger_rows[0], "active_electron_antineutrinos":0}
    check("reject_daughter_without_antineutrino", not balances_close(incomplete))
    incomplete = {**ledger_rows[0], "daughter_nonrest_budget_MeV":"0"}
    check("reject_missing_daughter_nonrest_energy", not balances_close(incomplete))
    duplicated = {**ledger_rows[0], "daughter_nonrest_budget_MeV":number(2*Decimal(ledger_rows[0]["daughter_nonrest_budget_MeV"]))}
    check("reject_duplicated_daughter_nonrest_energy", not balances_close(duplicated))
    wrong_unit = {**ledger_rows[0], "total_baryons":config["address"]}
    check("reject_address_as_baryon_count", not balances_close(wrong_unit))
    summary = {"address":config["address"], "prime_pool":primes,
               "common_source_baryons":common_baryons,
               "common_source_energy_MeV":number(source_energy),
               "per_daughter_nonrest_budget_MeV":number(release),
               "ledger":ledger_rows,
               "checks":{"passed":sum(checks.values()),"total":len(checks),"all_passed":all(checks.values()),"items":checks},
               "scope":"Static assembly and declared nucleon readouts with a shared source ledger; no time-dependent reaction or photon-transport simulation is executed by this dataset."}
    return {"assembly_trace.csv":csv_bytes(trace_rows),
            "component_instances.csv":csv_bytes(instance_rows),
            "component_counts.csv":csv_bytes(component_rows),
            "case_ledger.csv":csv_bytes(ledger_rows),
            "results.json":json_bytes(summary)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT/"reproduced")
    parser.add_argument("--check", action="store_true", help="Compare recalculated bytes with the distributed data directory")
    args = parser.parse_args()
    config=json.loads((ROOT/"inputs.json").read_text(encoding="utf-8"))
    generated=generate(config)
    args.output.mkdir(parents=True,exist_ok=True)
    for name,contents in generated.items():
        (args.output/name).write_bytes(contents)
    if args.check:
        for name,contents in generated.items():
            if (ROOT/"data"/name).read_bytes()!=contents:
                raise AssertionError("Reference mismatch: "+name)
    summary=json.loads(generated["results.json"])
    print(json.dumps({"all_passed":summary["checks"]["all_passed"],
                      "checks":summary["checks"]["total"],
                      "reference_byte_comparison":bool(args.check),
                      "output":str(args.output.resolve())},indent=2))


if __name__=="__main__":
    main()
