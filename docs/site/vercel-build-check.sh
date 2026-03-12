#!/bin/bash
# Vercel Ignored Build Step — always skip auto-deploy.
#
# All production deployments go through CI/CD pipelines (deploy-website.yml
# and release.yml) which handle git-crypt decryption before deploying via
# Vercel CLI. Vercel's auto-deploy (GitHub integration) cannot decrypt
# git-crypt files, so allowing it to build would deploy encrypted binary
# blobs as API source code, breaking all Edge functions.
#
# Exit codes (Vercel convention):
#   0 = skip build
#   1 = proceed with build

echo "Skip: all deployments handled by CI/CD pipeline (git-crypt required)"
exit 0
