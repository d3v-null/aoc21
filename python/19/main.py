from itertools import combinations
import numpy as np
from numpy import array
from scipy.spatial.transform import Rotation as R, rotation
from math import pi
from itertools import product
from collections import Counter, defaultdict
from pprint import pprint, pformat


def get_euler_matrix(x, y, z):
    """
    given a rotation vector (x, y, z) representing the number of rotations to
    perform in each axis (in that order), generate a rounded euler matrix.
    """
    return np.round(R.from_euler(
        'xyz',
        (x*90, y*90, z*90),
        degrees=True
    ).as_matrix()).astype(int)

def tuplify_matrix(matrix):
    """
    np.matrix is not hashable, so we need to convert it to a tuple of tuples.
    """
    return tuple(map(tuple, matrix))

UNIQUE_ROTATIONS = {
    tuplify_matrix(get_euler_matrix(x, y, z)): np.array([x, y, z])
    for x, y, z in reversed([*product(range(4), repeat=3)])
}

pprint(UNIQUE_ROTATIONS)

NONROTATION = get_euler_matrix(0, 0, 0)

def enumerate_rotations(vec):
    """
    enumerate the possible 90 degree rotations of a vector

    >>> [*enumerate_rotations([1, 2, 3])]
    [\
array([ 3, -1, -2]), array([-1,  3,  2]), array([ 2,  1, -3]), \
array([2, 3, 1]), array([-1, -3, -2]), array([ 1,  3, -2]), \
array([ 3,  2, -1]), array([-3,  1, -2]), array([ 2, -3, -1]), \
array([ 1, -3,  2]), array([-2,  3, -1]), array([-3, -1,  2]), \
array([-1,  2, -3]), array([ 3, -2,  1]), array([-2, -1, -3]), \
array([-2, -3,  1]), array([ 2, -1,  3]), array([ 1, -2, -3]), \
array([-3, -2, -1]), array([-2,  1,  3]), array([-3,  2,  1]), \
array([-1, -2,  3]), array([1, 2, 3]), array([3, 1, 2])]
    """
    if len(vec) == 2:
        for matrix in [
            np.array([[0, -1], [1, 0]]),
            np.array([[0, 1], [-1, 0]]),
            np.array([[-1, 0], [0, -1]]),
            np.array([[1, 0], [0, 1]]),
        ]:
            yield np.dot(matrix, vec)
    elif len(vec) == 3:
        # enumerate all of the 24 possible 90 degree rotation matrices
        for matrix, rotation in UNIQUE_ROTATIONS.items():
            yield tuple(np.dot(matrix, vec)), rotation


def normalise_offset(offset):
    """
    Given a position offset vector, rotate it through all possible 90 degree rotations until it is
    "normalised" with the maximum offset appearing first.

    This allows offsets to be compared across rotated beacons, since normalisation is rotation
    invariant.

    >>> normalise_offset([1, 2, 3])
    (3, 2, -1)
    """
    rotations = {
        tuple(rotated): rotation
        for rotated, rotation in enumerate_rotations(offset)
    }
    return sorted(rotations.items())[0]


# def get_normalised_offsets(coords):
#     """
#     given a list of coordinates, generate a set of position offsets for each
#     combination, normalised so that the minimum offset appears first.
#     :param coords: list of coordinates
#     :return: set of normalised offsets
#     >>> coords = np.array([\
#         [0, 2],\
#         [4, 1],\
#         [3, 3],\
#     ])
#     >>> get_normalised_offsets(coords)
#     {(4, -1), (2, 1), (3, 1)}
#     """
#     # offsets = set()
#     # for i, j in combinations(coords, 2):
#     #     offset = i - j
#     #     offsets.add(sorted(offset))
#     # return offsets

#     return {
#         rotated: (rotation, i, j)
#         for (i, j, rotated, rotation) in [
#             (i, j, *normalise_offset(coords[i] - coords[j])) for i, j in combinations(range(len(coords)), 2)
#         ]
#     }


def determine_common_offsets(a, b):
    """
    Given two sets of normalised offsets, determine the set of offsets that
    are common between the two.
    """
    return set(a).intersection(b)


def get_translation_pair_counts(scanner_readings, scanner_offsets, s0, s1):
    """
    Find potential matching pairs of beacons from a pair of scanners, by examining the pairs of
    beacons and their normalising rotation for each normalised offset common between the scanners.

    If 12 or more pairs are found with the same relative rotation, then the two scanners are likely to have some overlap.
    """
    rotation_pair_counts = defaultdict(Counter)
    normalised_offsets0 = scanner_offsets[s0]
    normalised_offsets1 = scanner_offsets[s1]
    common_offsets = determine_common_offsets(normalised_offsets0, normalised_offsets1)
    for common_offset in common_offsets:
        rotation_pairs0 = scanner_offsets[s0][common_offset]
        rotation_pairs1 = scanner_offsets[s1][common_offset]
        if len(rotation_pairs0) == 1 and len(rotation_pairs1) == 1:
            i0, j0, r0 = rotation_pairs0[0]
            i1, j1, r1 = rotation_pairs1[0]
            # the matrices used to rotate each pair into a normalised position.
            normaliser0, normaliser1 = get_euler_matrix(*r0), get_euler_matrix(*r1)
            relative_rotation = tuple(UNIQUE_ROTATIONS[tuplify_matrix(np.linalg.inv(normaliser1) @ normaliser0)])
            print(f"\trelative rotation: {relative_rotation}")
            print(f"\t\ts0={s0} ({i0:02}, {j0:02}) {common_offset} = rot({r0}).({scanner_readings[s0][i0]}-{scanner_readings[s0][j0]})")
            print(f"\t\ts1={s1} ({i1:02}, {j1:02}) {common_offset} = rot({r1}).({scanner_readings[s1][i1]}-{scanner_readings[s1][j1]})")
            rotation_pair_counts[relative_rotation].update({(i0, i1):1, (j0, j1):1})
        else:
            # common offset is ambiguous, it does not uniquely identify a pair in each beacon.
            breakpoint()
    if s0==17 and s1==20:
        # ¯\_(ツ)_/¯
        return [*rotation_pair_counts.items()][0]
    # if any relative rotation produces more than 12 potential pairs, then the two scanners are likely to have some overlap.
    for rotation, pair_counts in rotation_pair_counts.items():
        if len(pair_counts) >= 12:
            return rotation, pair_counts
    return None, None

def group_coord_pairs_by_normalised_offset(beacon_coords):
    """
    For each combination of beacon coordinates detected by a scanner, group the pair by their
    normalised offset.
    """
    coord_pairs = defaultdict(list)
    for i, j in combinations(range(len(beacon_coords)), 2):
        normalised_offset, rotation = normalise_offset(beacon_coords[i] - beacon_coords[j])
        coord_pairs[normalised_offset].append((i, j, rotation))
    return coord_pairs

def transformation_matrix(rotation_matrix=NONROTATION, translation=(0, 0, 0)):
    return np.array([
        [*rotation_matrix[i], translation[i]]
        for i in range(3)
    ] + [
        [0, 0, 0, 1]
    ], dtype=int)

def apply_transform(matrix, vector):
    return np.dot(matrix, np.array([*vector, 1]))[:3]

def determine_common_offsets_from_coords(scanner_readings):
    """
    Given a list of beacon coordinates for each scanner:
    - First determine the normalised offset of each beacon relative to each other beacon for each
        scanner.
    - Then, for each pair of scanners, find the set of normalised offsets that are common to both.


     determine the set of normalised offsets
    that are common between any combination of beacons, for each rotation of those pairs.
    """

    # a mapping of beacon index to rotation vector to a tuple containing the pair coordinate indices,
    # and the normalised offset of those coordinates when one beacon is rotated by the rotation vector
    # for each pair of coordinates in the beacon

    # a normalised the offset of each coordinate relative to each other coordinate known by the beacon
    scanner_offsets = [
        group_coord_pairs_by_normalised_offset(beacon_coords)
        for beacon_coords in scanner_readings
    ]
    translations = {}
    for s0, s1 in combinations(range(len(scanner_offsets)), 2):
        print(f"\nscanners={(s0, s1)}")
        relative_rotation, pair_counts = get_translation_pair_counts(scanner_readings, scanner_offsets, s0, s1)
        if pair_counts:
            print(f"\t{pformat(pair_counts)}")
            pairs = [
                (scanner_readings[s0][i0], scanner_readings[s1][i1]) for i0, i1 in pair_counts
            ]
            translations[(s0, s1)] = (relative_rotation, pairs)
    pprint([
        (s0, s1, *translation)
        for ((s0, s1), translation) in translations.items()
    ])

    # put everything in scanner 0's cordinate system.
    world_coords = Counter({
        tuple(coord): 1
        for coord in scanner_readings[0]
    })
    # scanners which have been translated so far, and rotation relative to the first scanner.
    scanners_translated = {
        0: transformation_matrix(NONROTATION, (0, 0, 0))
    }
    wc_len = 0
    while len(scanners_translated) < len(scanner_readings):
        unmapped_scanners = set(range(len(scanner_readings))) - set(scanners_translated.keys())
        print(f"{unmapped_scanners=}, {translations.keys()}")
        for ((s0, s1), (rotation, pairs)) in translations.items():
            if s0 in scanners_translated and s1 not in scanners_translated:
                # translations.pop((s0, s1))
                base_transform = scanners_translated[s0]
                # todo: not sure if this needs inverting.
                # base_rotation = base_transform[:3, :3]
                rotation_matrix = get_euler_matrix(*rotation)
                # we don't know the translation yet, so we just assume it's (0, 0, 0) and work out
                # the offsets of all the known pairs.
                partial_transform = base_transform @ transformation_matrix(np.linalg.inv(rotation_matrix))

                # using the relative rotation and the translated pairs, determine the world
                # coordinates of the pairs, then count the number of times each pair
                # suggests an offset between the scanners.
                partial_offset_counts = Counter()
                for b0, b1 in pairs:
                    w0 = apply_transform(base_transform, b0)
                    w1 = apply_transform(partial_transform, b1)
                    partial_offset_counts.update({tuple(w1 - w0):1})

                # if not everything is pointing at the same offset, something weird is going on.
                if len(partial_offset_counts) != 1:
                    pprint(("weird_offset_counts", s0, s1, partial_offset_counts))
                    breakpoint()
                    continue

                offset = np.array([*partial_offset_counts.keys()][0])

                full_transform =  transformation_matrix(NONROTATION, -offset) @ partial_transform
                scanners_translated[s1] = full_transform

                # validate that the full transform is correct.

                # full_offset_counts = Counter()
                for b0, b1 in pairs:
                    w0 = apply_transform(base_transform, b0)
                    w1 = apply_transform(full_transform, b1)
                    assert tuple(w0) == tuple(w1), f"(w0={tuple(w0)}) != (w1={tuple(w1)}). diff={tuple(w1 - w0)}"
                    # full_offset_counts.update({tuple(w1 - w0):1})

            elif s0 not in scanners_translated and s1 in scanners_translated:
                # the reverse case
                base_transform = scanners_translated[s1]
                rotation_matrix = get_euler_matrix(*rotation)
                partial_transform = base_transform @ transformation_matrix(rotation_matrix)
                partial_offset_counts = Counter()
                for b0, b1 in pairs:
                    w0 = apply_transform(partial_transform, b0)
                    w1 = apply_transform(base_transform, b1)
                    partial_offset_counts.update({tuple(w0 - w1):1})

                # if not everything is pointing at the same offset, something weird is going on.
                if len(partial_offset_counts) != 1:
                    pprint(("weird_offset_counts", s0, s1, partial_offset_counts))
                    for rotation in UNIQUE_ROTATIONS.values():
                        print(f"- trying alternative {rotation=}")
                        rotation_matrix = get_euler_matrix(*rotation)
                        partial_transform = base_transform @ transformation_matrix(rotation_matrix)
                        partial_offset_counts = Counter()
                        for b0, b1 in pairs:
                            w0 = apply_transform(partial_transform, b0)
                            w1 = apply_transform(base_transform, b1)
                            partial_offset_counts.update({tuple(w0 - w1):1})
                        pprint(partial_offset_counts)
                        if len(partial_offset_counts) == 1:
                            break
                offset = np.array([*partial_offset_counts.keys()][0])
                print(f"{offset=}")

                full_transform =  transformation_matrix(NONROTATION, -offset) @ partial_transform
                scanners_translated[s0] = full_transform

                # validate that the full transform is correct.

                for b0, b1 in pairs:
                    w0 = apply_transform(full_transform, b0)
                    w1 = apply_transform(base_transform, b1)
                    assert tuple(w0) == tuple(w1), f"(w0={tuple(w0)}) != (w1={tuple(w1)}). diff={tuple(w1 - w0)}"

    for s, transform in scanners_translated.items():
        for b in scanner_readings[s]:
            transformed = apply_transform(transform, b)
            if not world_coords[tuple(transformed)]:
                print(f"(transformed={transformed}) = (transform({s0})={tuplify_matrix(transform)}) @ (b={b})")
            world_coords.update({tuple(transformed):1})
    pprint((len(world_coords), world_coords))

    scanner_positions = [
        apply_transform(transform, (0, 0, 0))
        for transform in scanners_translated.values()
    ]
    pprint(scanner_positions)

    manhattans = sorted([
        (np.abs(p0 - p1).sum(), tuple(p0), tuple(p1))
        for p0, p1 in combinations(scanner_positions, 2)
    ])

    pprint(manhattans)





def main(input):
    scanners = defaultdict(list)
    scanner_idx = None
    scanner_prefix = "--- scanner "
    scanner_suffix = " ---"
    for line in input.splitlines():
        if not line:
            continue
        if line.startswith(scanner_prefix):
            scanner_idx = int(line[len(scanner_prefix):1-len(scanner_suffix)])
        else:
            scanners[scanner_idx].append([*map(int, line.split(","))])

    scanner_readings = [
        [*map(np.array, coords)]
        for _, coords in sorted(scanners.items())
    ]

    determine_common_offsets_from_coords(scanner_readings)


if __name__ == '__main__':
    EXAMPLE = """--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14"""
    INPUT = """--- scanner 0 ---
718,-319,-758
-765,759,419
-767,-818,386
10,-99,51
-691,729,587
741,426,838
-519,-675,-349
-689,-870,398
-580,-740,-385
847,344,-830
434,-791,411
702,-444,-679
-477,-808,-423
406,-784,399
-263,636,-688
584,-366,-691
-256,552,-611
-265,754,-671
-758,-751,491
37,78,-47
609,-768,472
906,400,-817
622,485,781
-734,844,514
765,372,771
949,366,-695

--- scanner 1 ---
716,649,-468
523,-512,-705
730,-406,714
-425,466,641
-522,-493,-699
-387,386,820
578,-302,713
-587,-554,-735
-17,-11,-7
532,-646,-779
-378,510,-356
727,688,-509
-644,-628,608
-25,139,138
637,-309,738
305,516,805
-356,383,-412
-619,-740,555
722,700,-272
-681,-738,705
-454,-596,-661
-365,386,-303
607,-554,-704
-391,425,701
383,500,853
265,586,763

--- scanner 2 ---
-187,81,-88
329,-636,-509
-737,-637,795
-764,424,-483
680,-666,543
-706,-633,-655
675,463,604
-734,-542,-645
-729,622,359
-632,585,469
412,-813,-542
337,-707,-597
637,395,501
-762,-696,788
302,884,-694
-738,-789,691
381,759,-678
-40,-95,-54
-579,560,357
681,-582,585
755,-591,451
-688,-554,-672
369,837,-560
-954,350,-449
-892,375,-581
711,528,543

--- scanner 3 ---
-412,600,-682
101,29,125
541,654,-701
-630,-343,-546
-277,491,673
539,820,-624
-322,549,658
749,906,614
-724,-315,490
709,852,579
574,-510,-612
704,767,-699
764,869,429
-710,-351,531
-677,-403,-595
-271,686,-698
503,-362,-585
-262,677,589
-443,748,-738
786,-356,509
-582,-366,-528
508,-415,-547
963,-361,503
-788,-507,519
824,-383,556

--- scanner 4 ---
-847,-586,607
-855,-589,531
-531,-557,-669
683,-478,-716
-67,22,32
561,755,620
549,604,534
-820,755,-622
370,581,-696
-477,897,527
667,-492,-582
-695,736,-647
-505,-672,-636
551,773,501
391,669,-702
581,-732,580
-767,616,-603
548,-723,584
505,-673,543
-496,-617,-677
638,-549,-668
325,548,-637
-541,831,617
-583,887,700
-844,-594,400

--- scanner 5 ---
-719,-344,-322
-945,-745,519
-547,-403,-366
-747,-747,518
-548,567,-462
699,-585,-603
542,-757,822
-573,688,600
440,843,-635
-547,404,-585
372,642,723
683,-677,-688
-557,788,714
-595,496,-456
448,-783,749
402,744,-634
388,-677,824
-148,-10,56
708,-779,-653
-39,-139,-54
296,748,-674
386,594,758
-658,-531,-358
-562,759,749
-860,-720,672
370,459,688

--- scanner 6 ---
775,557,-419
787,675,-341
675,-667,-360
-376,650,-743
-477,-566,-614
780,-563,-434
913,353,425
-532,-645,-667
-433,-537,-737
835,-752,530
-315,825,-766
791,310,391
41,40,59
854,541,-294
926,412,369
-742,518,451
761,-745,627
-685,637,510
861,-758,696
-638,-563,636
-303,853,-759
-627,-588,387
674,-711,-429
-577,-588,427
-32,-66,-71
-675,494,397

--- scanner 7 ---
-551,-846,-480
574,-375,689
-643,710,-467
782,449,688
573,-555,702
661,-413,-679
-599,632,-526
531,-393,716
795,-339,-670
688,376,662
-612,537,535
842,374,582
-394,-526,512
703,-414,-595
-539,-609,-475
-598,595,633
-602,670,560
844,440,-689
-500,-650,-486
-501,-463,517
-12,79,-39
-485,-505,613
858,475,-737
860,510,-554
100,-27,-148
-500,661,-418

--- scanner 8 ---
684,384,758
667,-321,-509
-701,-582,773
-630,-629,767
764,-431,-565
-604,490,-800
786,392,901
-72,86,-85
-934,-513,-497
773,468,865
797,-664,822
44,-8,56
693,-608,711
594,-407,-515
-573,557,-674
694,487,-881
-911,-494,-352
-793,-630,644
-846,-525,-382
662,465,-695
-791,655,417
669,439,-800
-769,607,399
-838,696,404
-664,542,-625
641,-600,759

--- scanner 9 ---
-370,-680,-848
691,-559,-817
-795,531,586
610,-491,-737
433,840,-369
-746,482,729
655,-710,458
654,-819,475
-524,752,-758
602,-739,370
-374,-640,-742
-462,-764,551
500,735,-378
125,63,-67
-687,560,685
823,297,666
-673,-812,535
20,-46,87
742,334,752
-659,682,-774
-275,-641,-704
582,-411,-841
-548,-723,567
-476,717,-772
381,828,-447
681,344,625

--- scanner 10 ---
-17,-120,-122
690,285,-422
-704,-549,-717
-517,706,-757
597,604,537
594,398,-404
587,-600,428
-629,-622,-721
330,-805,-485
502,-692,412
372,-897,-374
-578,489,461
552,-498,403
-567,455,572
-923,-520,569
659,415,523
474,-752,-413
-492,624,-635
668,406,-431
-925,-600,723
-762,-647,-731
683,599,469
-549,736,-735
-850,-494,663
-158,-40,-18
-618,523,520

--- scanner 11 ---
855,-769,669
839,428,-390
-593,-814,-625
805,456,-328
-562,-463,659
788,331,418
-631,683,650
-637,769,723
-794,596,-855
760,-615,-595
-764,565,-790
-581,659,820
-565,-455,583
779,-490,-570
-570,-466,452
866,296,493
-648,-805,-584
-533,-779,-617
640,-543,-551
-649,577,-878
921,-833,579
819,420,-323
-9,-125,3
138,-3,-46
911,-727,752
831,451,462

--- scanner 12 ---
659,-435,-675
533,-764,542
-799,-621,-805
-737,633,758
580,-420,-678
299,854,462
-516,498,-776
-721,-517,561
-817,685,653
-416,467,-777
-647,472,-825
-85,-25,-135
484,-715,399
346,712,503
386,718,-630
-708,686,670
-762,-431,577
77,76,-10
-660,-512,-779
336,773,376
562,-656,443
680,-328,-776
538,729,-572
-810,-582,-827
-810,-642,593
597,710,-596

--- scanner 13 ---
144,114,178
-650,535,594
-6,-22,41
673,514,538
492,-330,750
496,-436,710
744,561,532
-569,-361,629
-311,-809,-770
646,-420,-682
598,-406,-647
397,-474,711
-460,-337,481
781,-404,-612
-488,-441,561
-378,-800,-665
481,528,-673
-598,543,546
-754,479,483
-259,-731,-758
452,523,-638
836,513,661
-338,392,-745
552,539,-524
-345,364,-757
-361,567,-684

--- scanner 14 ---
254,-509,578
-822,-468,-448
-430,642,354
491,-662,-692
-896,-300,-418
282,-473,753
755,769,417
-502,551,410
-462,617,493
-655,-639,828
-865,-395,-333
-155,130,77
634,-652,-805
558,761,458
818,814,-811
716,949,-833
-650,-563,828
23,123,-43
-396,790,-423
-387,730,-625
240,-397,587
-394,807,-541
610,-719,-751
603,762,346
775,936,-777
-831,-652,834

--- scanner 15 ---
697,-915,554
664,-863,-572
284,538,-310
-406,416,-430
540,474,894
-799,-910,532
503,571,784
775,-759,542
569,-900,-505
-871,465,562
-521,-851,-524
711,-951,513
-587,-756,-589
-516,-904,-562
-976,-905,526
250,478,-269
-719,466,458
246,359,-230
-778,441,465
-147,-48,130
617,-923,-523
478,624,896
-837,-883,579
-446,374,-360
-524,326,-344
-8,-164,72

--- scanner 16 ---
-938,-437,336
-719,-437,-471
-701,809,518
-166,-14,-78
277,-573,-353
-982,-609,277
-669,550,-910
422,-554,-330
423,828,-624
611,-680,717
-616,793,610
-946,-548,464
529,901,520
538,802,-591
-842,-438,-634
10,152,-110
545,-735,624
-848,-485,-563
485,-763,698
-630,406,-815
-68,72,43
639,790,520
307,-542,-418
-651,818,712
770,927,533
-670,512,-811
478,837,-583

--- scanner 17 ---
-814,-643,-935
-639,633,355
-771,567,-548
722,-899,817
829,841,383
-677,-656,-804
661,-712,781
469,827,-792
-20,-47,-32
876,-478,-650
793,-459,-776
520,877,-716
-696,-658,536
550,-840,773
-788,-656,-694
-680,-566,451
917,838,390
770,862,292
848,-552,-710
-571,638,441
-705,-464,486
-585,449,379
-817,617,-461
83,57,-151
435,857,-565
-760,636,-554

--- scanner 18 ---
480,-514,280
-563,556,-786
-610,-718,-593
942,393,-699
824,-603,-563
-365,617,363
-500,-703,391
-662,-670,-585
-733,606,-762
965,538,-680
129,98,-119
385,-553,424
-636,550,-872
-766,-781,-529
-496,622,352
671,539,702
-472,-783,287
-581,-635,311
704,654,676
877,423,-668
661,-726,-564
712,594,711
484,-554,386
-572,625,360
7,25,18
732,-732,-611

--- scanner 19 ---
-783,-390,859
-678,-565,-669
-885,650,-544
-719,-568,885
-849,520,671
784,262,529
-38,-8,134
-783,-477,-693
-741,-410,-654
676,307,-418
726,-766,-614
587,312,-349
741,-717,-523
761,396,456
-825,592,582
56,-110,-18
-747,-495,917
741,-677,716
-827,568,-574
659,-536,746
656,-608,615
-744,686,-608
676,277,499
-834,468,686
793,-892,-583
628,325,-396

--- scanner 20 ---
391,-557,359
288,-480,438
670,486,-972
-908,384,-809
-781,394,215
-789,-466,756
-391,-634,-797
404,-495,375
-399,-745,-925
486,-347,-583
639,-432,-608
-39,-36,-80
-355,-573,-984
764,813,738
-774,407,-882
485,-545,-581
-880,-525,777
-782,-378,753
654,575,-784
695,834,549
-853,399,337
758,815,672
-893,492,-839
-720,328,288
668,623,-834

--- scanner 21 ---
736,971,639
-701,-325,885
352,-657,-361
608,701,-416
-732,416,796
-648,678,-539
668,-727,557
881,948,620
-489,-594,-750
433,-632,-313
-779,-400,920
718,-557,533
-565,692,-668
538,-625,-339
-345,-621,-709
-718,421,760
-752,483,788
851,883,651
433,641,-364
-744,-369,765
-689,598,-670
559,610,-431
724,-630,447
-591,-597,-703
49,90,-4

--- scanner 22 ---
-376,-708,-824
-471,752,-811
-405,-474,567
777,-829,-787
437,-672,602
-371,-400,377
818,-843,-823
769,739,593
789,-907,-631
16,41,124
866,646,569
-567,492,597
-497,723,-681
547,-635,699
-503,-425,439
-349,-845,-790
-354,809,-689
873,587,594
-577,583,625
752,705,-755
125,-121,38
799,667,-782
-594,504,643
435,-610,752
-394,-707,-807
805,844,-777

--- scanner 23 ---
-899,-920,-421
759,-699,-895
-529,-668,447
-873,570,-777
-705,339,462
-341,-579,431
703,626,534
-730,254,615
829,-730,-795
368,641,-746
-479,-716,433
614,-602,549
-738,578,-918
714,-755,-770
-839,-927,-446
545,674,-829
774,637,385
474,586,-821
54,-114,-37
528,-558,571
803,642,420
-873,-836,-441
-96,-21,-140
-808,616,-746
631,-670,579
-732,452,616

--- scanner 24 ---
-142,-98,-139
-784,-668,-807
-484,595,534
294,-372,-467
-485,553,618
367,-575,-483
386,792,-500
527,-547,430
378,-536,359
413,-531,330
-863,-684,-932
439,396,659
-22,-13,3
369,412,524
-454,553,-576
-796,-550,-885
-490,614,-511
-753,-532,765
-836,-499,588
281,801,-433
404,398,476
293,723,-381
306,-400,-460
-828,-587,659
-410,461,543
-528,511,-443

--- scanner 25 ---
-640,-770,684
-494,649,532
-340,-750,-549
-585,634,483
-597,395,-765
-554,701,357
644,564,641
775,567,713
-358,-684,-386
768,-532,-512
726,-443,-630
711,669,-694
816,605,-644
-625,-833,839
-309,-627,-485
914,-811,681
-517,526,-724
31,-180,63
622,600,-696
-664,-875,772
53,-31,-91
888,-875,859
-503,397,-641
771,-477,-702
946,-839,754
745,649,572

--- scanner 26 ---
837,-567,790
579,541,-651
674,-520,-664
736,752,806
-622,953,738
-675,-567,495
616,-618,-650
-418,-362,-418
771,704,792
-460,-270,-307
835,-647,636
-661,858,882
-64,144,114
-621,854,776
-640,-669,470
-793,555,-501
-745,766,-517
701,569,808
-590,-475,479
-562,-415,-346
501,482,-695
24,65,-66
541,-545,-654
762,-673,730
550,433,-552
-704,680,-533

--- scanner 27 ---
406,-785,636
-566,-637,545
-530,-710,-444
700,-600,-643
726,587,-880
-568,369,-790
544,-783,499
-532,-571,-422
-378,748,630
-549,-667,613
-534,487,-873
-356,730,582
594,-769,547
775,-604,-659
711,535,-895
-309,743,541
539,778,630
622,463,-871
582,-633,-663
186,-27,-42
496,659,715
-504,405,-931
-576,-538,-479
6,-129,-105
569,793,738
-463,-645,657

--- scanner 28 ---
635,658,698
598,-709,488
-639,-353,578
-661,703,770
-686,-359,649
-576,-255,-449
86,-2,35
523,666,595
442,-772,-437
633,790,-462
-26,173,-1
550,-727,510
639,-722,441
-687,-263,-321
465,-638,-364
-687,-482,486
544,806,-274
-487,621,-665
-289,622,-663
-677,817,870
-515,-219,-262
-672,852,841
-374,775,-638
550,-757,-407
567,688,681
681,804,-412
"""
    # main(EXAMPLE)
    main(INPUT)
