"""Deterministic full-corpus recode of the criterion-sensitive axes (task, environment),
plus candidate screens for physics claims and eligibility.

Rules implement RECODE_INSTRUCTIONS.md v1.0 as applied by the two blind human recodes:
  * Task: a study counts as design work only if the abstract describes searching the
    mix-design space (optimizing, inverting or selecting mixes). Metaheuristic tuning of a
    predictor's hyperparameters ("PSO-optimized XGBoost") is prediction.
  * Environment: an environmental function counts only if it is quantified or modelled
    (an output, objective, constraint, inventory or reported number). Framing words such as
    "sustainable", "eco-friendly" or "green" earn nothing.
Usage: python3 recode_rules.py corpus669_abstracts.csv out.csv
"""
import csv, re, sys

def low(s): return (s or '').lower()

# ---------------- task ----------------
EXP_SEL = re.compile(r'\b(active learning|sequential learning|bayesian optimi[sz]ation|closed[- ]loop|self[- ]driving|autonomous (lab|experiment)|adaptive (design|sampling|experiment))')
INVERSE = re.compile(r'\b(inverse (mix |material )?design|reverse design|inverse (problem|model(l)?ing|prediction)|generative (design|model)|target[- ](property|strength)[- ](driven|oriented) design|design(s|ing)? (new|novel|candidate) (mix|mixture|formulation)s?|recommend(s|ed|ation|er)? (of )?(optimal |suitable )?(mix|mixture|proportion))')
MOO = re.compile(r'\b(multi[- ]?objective|many[- ]objective|pareto|nsga|mopso|moea|trade[- ]?offs? (between|among) (strength|cost|carbon|co2))')
MIXOPT = re.compile(r'(optimi[sz](e|ed|es|ing|ation)[^.]{0,60}\b(mix|mixture|proportion|formulation|composition|dosage|design|binder|activator content|ratio)s?\b'
                    r'|\b(mix|mixture|proportion|formulation)s?( design)? optimi[sz]'
                    r'|optimal (mix|mixture|proportion|formulation|dosage|combination|ratio)s?'
                    r'|(maximi[sz]e|minimi[sz]e)[^.]{0,40}(strength|cost|carbon|co2|emission)'
                    r'|(genetic algorithm|particle swarm|metaheuristic|evolutionary algorithm|grey wolf|whale optimi)[^.]{0,80}(to (find|identify|determine|search|obtain|optimi[sz]e) (the )?(optimal|best) (mix|mixture|proportion|design))'
                    r'|response surface)')
HYPER_ONLY = re.compile(r'\b(hyper[- ]?parameters?|tun(e|ed|ing) (the )?(model|hyper)|(pso|ga|gwo|woa|firefly|sparrow|grey wolf|whale|particle swarm|genetic algorithm|metaheuristic)[- ](optimi[sz]ed|tuned|based|enhanced)? ?(xgboost|ann|svr|svm|random forest|neural|model|lightgbm|catboost|elm|regression))')
CLASSIF = re.compile(r'\b(classif(y|ication|ier)|categori[sz]ation)\b')
IMAGE = re.compile(r'\b(image|images|micrograph|sem image|ct scan|x-ray tomograph|microstructur(e|al) (analysis|segmentation|recognition)|segmentation|convolutional[^.]{0,30}(image|micrograph))')

def code_task(t):
    if EXP_SEL.search(t): return 'experiment-selection'
    if INVERSE.search(t): return 'inverse-design'
    if MOO.search(t) and (MIXOPT.search(t) or re.search(r'(mix|mixture|proportion|design)', t)): return 'multi-objective-optimization'
    if MIXOPT.search(t):
        # metaheuristic hyperparameter tuning alone is prediction
        hits = [m.group(0) for m in MIXOPT.finditer(t)]
        if all(re.search(r'(hyper|model|algorithm)', h) for h in hits) and HYPER_ONLY.search(t): return 'prediction'
        return 'optimization'
    if IMAGE.search(t) and re.search(r'(image|micrograph|segmentation|tomograph)', t): return 'microstructure/image-analysis'
    if CLASSIF.search(t) and not re.search(r'(predict|regression|estimat)', t): return 'classification'
    return 'prediction'

DESIGN = {'experiment-selection', 'inverse-design', 'multi-objective-optimization', 'optimization'}

# ---------------- environment ----------------
ENV_Q = re.compile(r'(co2|co₂|carbon (emission|footprint|dioxide|intensity|content)|embodied (carbon|energy|co2)|global warming potential|\bgwp\b|life[- ]cycle (assessment|analysis|inventory)|\blca\b|greenhouse gas|\bghg\b|eco[- ]?efficiency|energy (consumption|demand|use|intensity)|environmental (impact|index|indicator|cost|performance|load|burden)s?)')
QUANT_CTX = re.compile(r'(\d[\d.,]*\s*(%|kg|t\b|mj|kwh|percent)|reduc(e|ed|es|tion|ing)[^.]{0,30}by|object(ive|ives)|constraint|minimi[sz]|optimi[sz]|predict(ed|ing|ion|s)?|estimat|calculat|quantif|assess(ed|ment)?|evaluat|model(l)?(ed|ing)|inventory|indicator|index|lower|higher|compared)')
COST_Q = re.compile(r'(cost|price|economic)[^.]{0,60}(\d|objective|minimi[sz]|optimi[sz]|reduc|lower|predict|estimat|calculat|analys)|(\d[\d.,]*\s*(\$|usd|yuan|€|cny|inr)|\$\s*\d)')
WASTE_Q = re.compile(r'(\d[\d.,]*\s*%[^.]{0,40}(replace|waste|by-product|tailing|slag|ash|recycled|substitut)|(replace|substitut|incorporat|utili[sz])[^.]{0,40}\d[\d.,]*\s*%|waste (utili[sz]ation|content|ratio|dosage) (of|up to)?\s*\d)')
DUR_Q = re.compile(r'\b(durability|chloride|carbonation|sulfate|sulphate|freeze[- ]thaw|acid (attack|resistance)|shrinkage|creep|corrosion|permeability|water absorption|leaching|efflorescence)\b')

def code_env(t):
    s = set()
    for sent in re.split(r'(?<=[.;])\s+', t):
        if ENV_Q.search(sent) and QUANT_CTX.search(sent):
            s.add('LCA' if re.search(r'life[- ]cycle|\blca\b', sent) else 'carbon')
        if COST_Q.search(sent): s.add('cost')
        if WASTE_Q.search(sent): s.add('waste-valorization')
        if DUR_Q.search(sent) and re.search(r'(predict|model|estimat|resistance|depth|coefficient|loss|rate)', sent): s.add('durability')
    return ';'.join(sorted(s)) if s else 'none-explicit'

# ---------------- physics-claim screen ----------------
PHYS = re.compile(r'(physics[- ](informed|guided|based|constrained|embedded|aware)|chemistry[- ](informed|guided|aware)|knowledge[- ](guided|informed|driven|embedded|graph)|domain[- ]knowledge|thermodynamic (model|calculation|simulation)|gems\b|molecular dynamics|density functional|\bdft\b|first[- ]principles|governing equation|mechanis(m|tic)[- ](informed|guided|based model)|pinn|physical (law|constraint|consistency)|monotonic(ity)? constraint|hybrid (physics|mechanistic)|finite element[^.]{0,40}(machine learning|neural|surrogate)|kinetic model|hydration model|reaction (kinetics|model)|symbolic regression[^.]{0,40}physic|prior knowledge)')

# ---------------- eligibility screen ----------------
ML = re.compile(r'(machine learning|deep learning|neural network|\bann\b|\bcnn\b|lstm|random forest|xgboost|lightgbm|catboost|gradient boost|support vector|\bsvr\b|\bsvm\b|decision tree|regression tree|gaussian process|ensemble|artificial intelligence|\bai\b|data[- ]driven|gene expression programming|\bgep\b|\bmep\b|symbolic regression|transformer|k[- ]nearest|bayesian|genetic programming|fuzzy|anfis|boosting|predictive model|surrogate model|metaheuristic|large language model|\bllm\b)')
AAM = re.compile(r'(geopolymer|alkali[- ]activat|\baam|\baac\b|\baas\b|one[- ]part|alkaline activat|activated slag|activated fly ash|inorganic polymer|soil stabili[sz]|stabili[sz]ed (soil|clay)|fly ash[- ]based|slag[- ]based|metakaolin|red mud|tailing|low[- ]carbon (binder|concrete|cement)|cementitious)')
REVIEW = re.compile(r'(\bthis (review|survey)|systematic review|state[- ]of[- ]the[- ]art review|literature review|bibliometric|scientometric|critical review|comprehensive review|we review|is reviewed|are reviewed|critical synthesis|meta[- ]analysis)')
OFFTOPIC = re.compile(r'(remote sensing|satellite|sar imagery|building damage|change detection|traffic|power grid)')

def screen_elig(title, t):
    flags = []
    if not ML.search(t): flags.append('no-ML-term')
    if not AAM.search(t): flags.append('no-AAM-term')
    if REVIEW.search(t) or re.search(r'\breview\b', low(title)): flags.append('review')
    if OFFTOPIC.search(t): flags.append('off-topic-term')
    return ';'.join(flags)

def main(src, dst):
    rows = list(csv.DictReader(open(src, encoding='utf-8')))
    for r in rows:
        t = low(r['title'] + '. ' + r.get('abstract', ''))
        r['R_task'] = code_task(t)
        r['R_design'] = 'Y' if r['R_task'] in DESIGN else 'N'
        r['R_env'] = code_env(t)
        r['R_env_none'] = 'Y' if r['R_env'] == 'none-explicit' else 'N'
        r['R_phys_candidate'] = 'Y' if PHYS.search(t) else 'N'
        r['R_elig_flags'] = screen_elig(r['title'], t)
        r['R_basis'] = 'title+abstract' if r.get('abstract') else 'title-only'
    with open(dst, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
