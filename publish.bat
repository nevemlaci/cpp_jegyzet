mdbook build
git add .
git commit -m %1
git push
git subtree push --prefix book origin book