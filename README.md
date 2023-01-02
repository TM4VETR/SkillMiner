# SkillMiner

SkillMiner is used for a generic extraction of skills. It wraps spacy and PhraseMatcher.

## Input 

SkillMiner currently takes two arguments: ``-t, --terminologies`` which stores a comma-separated list of matchers for skills and ``-p, --path`` which refers to the path to them.

See ``SkillTest.sh`` in project ExamplePipelines.

## Output

This pipeline element outputs the annotated document.

## Generating Matcher

The matchers are stored in two files, for example:

```
pickle.dump(matcher, open("ba.map", 'wb'))
pickle.dump (nlp.vocab.strings, open("ba-v.map", 'wb'))
``` 

The matcher is a spacy Source PhraseMatcher, see https://spacy.io/api/phrasematcher. For example:

``` 
matcher = PhraseMatcher(nlp.vocab)
elmts = nlp.pipe(suchworte.keys())
for d in elmts:
    matcher.add(suchworte[str(d)], [d] )
```
