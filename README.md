# cosmoshub-3

# Step 0. Build Docker
```bash
./build-gaiadebug.sh v2.0.1
```

# Step 1. Verify migrated genesis.json
```bash
jq -S -c -M '' exported-hub3.json | shasum -a 256

> 3b38465931f57b004cef4196c77d8fd4d78c6a7ea1d0d23dc784ce65b7856a09
```

# Step 2. Run Reformat Script
```bash
python3 reformat.py  exported-hub3.json

jq -S -c -M '' genesis.json | shasum -a 256

> d2ef50819991406f264d8c20a1ab5aad1a41a2c874883b59182ee9c327a5b2a8
```

# Step 3a. Test New Genesis.json (Skip if already have node)

```bash
# Make Node Folder
mkdir -p node/

# Run Init
docker run --rm -it \
  -w /app \
  --mount type=bind,src=$PWD/node,dst=/app \
  --entrypoint="gaiad" \
  cosmos-gaiadebug:v2.0.1 init testnode \
  --chain-id cosmoshub-3 \
  --home /app
# Copy Over genesis.json
sudo cp genesis.json node/config/genesis.json

```

# Step 3b. For Existing Nodes

```bash
docker run --rm -it \
  -w /app \
  --mount type=bind,src=$PWD/node,dst=/app \
  --entrypoint="gaiad" \
  cosmos-gaiadebug:v2.0.1 unsafe-reset-all \
  --home /app

```

# Step 4 Start the Chain

```bash
docker run --rm -it \
  -w /app \
  --mount type=bind,src=$PWD/node,dst=/app \
  --entrypoint="gaiad" \
  cosmos-gaiadebug:v2.0.1 start \
  --home /app
```
