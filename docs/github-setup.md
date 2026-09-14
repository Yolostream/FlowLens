# GitHub setup checklist

## 1. Prepare locally

1. Extract the starter package.
2. Replace every `Yolostream` placeholder.
3. Update the author and copyright text where appropriate.
4. Run the example and tests.

## 2. Create the repository

Create a public GitHub repository named `flowlens`. Do not initialize it with another README, license or `.gitignore` because those files are already included.

## 3. Push the starter

```bash
cd flowlens
git init
git add .
git commit -m "feat: initial FlowLens analyzer"
git branch -M main
git remote add origin https://github.com/Yolostream/flowlens.git
git push -u origin main
```

## 4. Configure community features

In repository settings:

- enable Issues and Discussions;
- enable private vulnerability reporting;
- enable branch protection for `main`;
- require the test workflow before merging;
- require pull requests instead of direct pushes;
- delete head branches automatically after merge.

## 5. Create labels

Recommended labels:

- `good first issue`
- `help wanted`
- `bug`
- `enhancement`
- `new rule`
- `parser`
- `documentation`
- `security`

## 6. Publish the first release

1. Confirm the test workflow passes.
2. Create an annotated tag: `git tag -a v0.1.0 -m "FlowLens 0.1.0"`.
3. Push it: `git push origin v0.1.0`.
4. Create a GitHub release from the tag using the matching changelog section.

## 7. Build genuine community evidence

Share the repository with Power Platform communities, ask for sanitized parser cases, respond to issues publicly and keep a visible roadmap. Record only authentic usage and contributions.
