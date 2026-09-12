#!/usr/bin/env python3
"""Provisional PTT envelope arithmetic; no input is an actual radio measurement."""
import argparse
import json
import math


def calculate(v_min=4.35, v_max=5.25, vf_max=1.5, drop_max=0.3,
              resistor=470.0, tolerance=0.01):
    values = (v_min, v_max, vf_max, drop_max, resistor, tolerance)
    if not all(math.isfinite(x) for x in values):
        raise ValueError('Inputs must be finite')
    if not (0 < v_min <= v_max and vf_max >= 0 and drop_max >= 0
            and resistor > 0 and 0 <= tolerance < 1):
        raise ValueError('Invalid voltage/resistance/tolerance envelope')
    r_min, r_max = resistor * (1-tolerance), resistor * (1+tolerance)
    i_min = max(0.0, v_min-vf_max-drop_max) / r_max
    # Zero LED/driver lower drop is deliberately conservative, not a device model.
    i_max = v_max / r_min
    result = {
        'status': 'proposed assumptions, not measured hardware',
        'led_min_mA': i_min*1000, 'led_upper_mA': i_max*1000,
        'resistor_power_upper_W': v_max*v_max/r_min,
        'led_5_to_30mA_envelope_pass': i_min >= .005 and i_max <= .030,
        'driver_drop_budget_V': drop_max,
        'driver_power_bound_W': i_max*drop_max,
        'required_BJT_base_mA_at_forced_beta_10': i_max/10*1000,
    }
    # Conditional driver study: VOH>=2.4V, VBE<=0.95V, 1k base/100k pulldown.
    base_min = (2.4-.95)/1010 - .95/99000
    result.update(base_current_lower_mA=base_min*1000,
                  forced_beta_upper=i_max/base_min,
                  logic_source_upper_mA=3.6/990*1000)
    # Proposed 480k total tolerance ±1%; full-temperature IC accuracy ±3%.
    nominal = 2**21 * 480000 / 50000 * 1e-6
    result.update(timer_nominal_s=nominal,
                  timer_lower_s=nominal*.99*.97,
                  timer_upper_s=nominal*1.01*1.03)
    # Table 1 code 7: top 1M, bottom 887k. ±1% TOTAL each.
    top, bottom, tol = 1e6, 887e3, .01
    lower = bottom*(1-tol)/(top*(1+tol)+bottom*(1-tol))
    upper = bottom*(1+tol)/(top*(1-tol)+bottom*(1+tol))
    # ±10nA DIV input at minimum 2.25V, conservative maximum Thevenin R.
    r_th_max = (top*bottom/(top+bottom))*(1+tol)
    leakage_fraction = 10e-9*r_th_max/2.25
    lower -= leakage_fraction
    upper += leakage_fraction
    result.update(div_ratio_lower=lower, div_ratio_upper=upper,
                  div_thevenin_upper_ohm=r_th_max,
                  div_code7_pass=(lower >= .46875-.015 and
                                  upper <= .46875+.015 and r_th_max <= 500000))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name, default in [('v-min', 4.35), ('v-max', 5.25), ('vf-max', 1.5),
                          ('drop-max', .3), ('resistor', 470.), ('tolerance', .01)]:
        parser.add_argument('--'+name, type=float, default=default)
    args = parser.parse_args()
    try:
        result = calculate(**vars(args))
    except ValueError as error:
        parser.error(str(error))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result['led_5_to_30mA_envelope_pass'] and result['div_code7_pass'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
