FROM ubuntu@sha256:008173c23f95b170204355c12626cb5a965d779a7e1283b09e9cffbb1bf33ca3 AS system-tools
ENV DEBIAN_FRONTEND=noninteractive
RUN --mount=type=bind,source=debs-system,target=/debs \
    --mount=type=bind,source=system.sha256,target=/debs.sha256 \
    cd / && sha256sum --check /debs.sha256 && \
    apt-get install -y --no-install-recommends /debs/*.deb && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/*
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

FROM system-tools AS gtest-tools
RUN --mount=type=bind,source=debs-gtest,target=/debs \
    --mount=type=bind,source=gtest.sha256,target=/debs.sha256 \
    cd / && sha256sum --check /debs.sha256 && \
    apt-get install -y --no-install-recommends /debs/*.deb && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/*

FROM system-tools AS python-tools
RUN --mount=type=bind,source=recipe/install.py,target=/recipe/install.py \
    --mount=type=bind,source=recipe/python.lock.json,target=/recipe/sources.lock.json \
    --mount=type=bind,source=tool-inputs/python,target=/inputs \
    python3 /recipe/install.py python
ENV PATH=/opt/python/bin:$PATH

FROM python-tools AS litex-tools
RUN --mount=type=bind,source=recipe/install.py,target=/recipe/install.py \
    --mount=type=bind,source=recipe/litex.lock.json,target=/recipe/sources.lock.json \
    --mount=type=bind,source=tool-inputs/litex,target=/inputs \
    --mount=type=bind,source=recipe/patches,target=/recipe/patches \
    python3 /recipe/install.py litex

FROM system-tools AS verilator-tools
RUN --mount=type=bind,source=recipe/install.py,target=/recipe/install.py \
    --mount=type=bind,source=recipe/verilator.lock.json,target=/recipe/sources.lock.json \
    --mount=type=bind,source=tool-inputs/verilator,target=/inputs \
    python3 /recipe/install.py verilator

FROM system-tools AS yosys-tools
RUN --mount=type=bind,source=recipe/install.py,target=/recipe/install.py \
    --mount=type=bind,source=recipe/yosys.lock.json,target=/recipe/sources.lock.json \
    --mount=type=bind,source=tool-inputs/yosys,target=/inputs \
    python3 /recipe/install.py yosys

FROM system-tools AS rv32-tools
RUN --mount=type=bind,source=recipe/install.py,target=/recipe/install.py \
    --mount=type=bind,source=recipe/rv32.lock.json,target=/recipe/sources.lock.json \
    --mount=type=bind,source=tool-inputs/rv32,target=/inputs \
    --mount=type=bind,source=recipe/ci_rv32_sdk.py,target=/recipe/ci_rv32_sdk.py \
    python3 /recipe/install.py rv32-sdk

FROM system-tools AS sv2v-tools
RUN --mount=type=bind,source=recipe/install.py,target=/recipe/install.py \
    --mount=type=bind,source=recipe/sv2v.lock.json,target=/recipe/sources.lock.json \
    --mount=type=bind,source=tool-inputs/sv2v,target=/inputs \
    python3 /recipe/install.py sv2v

FROM system-tools AS sbt-tools
RUN --mount=type=bind,source=recipe/install.py,target=/recipe/install.py \
    --mount=type=bind,source=recipe/sbt.lock.json,target=/recipe/sources.lock.json \
    --mount=type=bind,source=tool-inputs/sbt,target=/inputs \
    --mount=type=bind,source=recipe/sbt-repositories,target=/recipe/sbt-repositories \
    python3 /recipe/install.py sbt

FROM system-tools AS oracle-tools
RUN --mount=type=bind,source=recipe/install.py,target=/recipe/install.py \
    --mount=type=bind,source=recipe/oracle.lock.json,target=/recipe/sources.lock.json \
    --mount=type=bind,source=tool-inputs/oracle,target=/inputs \
    python3 /recipe/install.py tsn-gen

FROM system-tools AS node-tools
RUN --mount=type=bind,source=recipe/install.py,target=/recipe/install.py \
    --mount=type=bind,source=recipe/node.lock.json,target=/recipe/sources.lock.json \
    --mount=type=bind,source=tool-inputs/node,target=/inputs \
    python3 /recipe/install.py node

FROM system-tools AS gh-tools
RUN --mount=type=bind,source=recipe/install.py,target=/recipe/install.py \
    --mount=type=bind,source=recipe/gh.lock.json,target=/recipe/sources.lock.json \
    --mount=type=bind,source=tool-inputs/gh,target=/inputs \
    python3 /recipe/install.py gh

FROM gtest-tools AS validation-tools
COPY --from=litex-tools /opt/python /opt/python
COPY --from=verilator-tools /opt/verilator /opt/verilator
COPY --from=yosys-tools /opt/yosys /opt/yosys
COPY --from=rv32-tools /opt/rv32-sdk /opt/rv32-sdk
COPY --from=sv2v-tools /opt/sv2v /opt/sv2v
COPY --from=sbt-tools /opt/sbt /opt/sbt
COPY --from=sbt-tools /opt/sbt-cache /opt/sbt-cache
COPY --from=oracle-tools /opt/tsn-gen /opt/tsn-gen
COPY --from=node-tools /opt/node /opt/node
COPY --from=gh-tools /opt/gh /opt/gh
ENV PATH=/opt/node/bin:/opt/gh/bin:/opt/python/bin:/opt/verilator/bin:/opt/yosys/bin:/opt/rv32-sdk/bin:/opt/sv2v/bin:/opt/sbt/bin:$PATH
ENV MILAN_RV32_CC=/opt/rv32-sdk/bin/riscv32-linux-gcc
ENV TSN_GEN_ROOT=/opt/tsn-gen
ENV VERILATOR_JOBS=2
ENV COURSIER_CACHE=/opt/sbt-cache/coursier
ENV SBT_OPTS="-Dsbt.boot.directory=/opt/sbt-cache/boot -Dsbt.global.base=/opt/sbt-cache/global -Dsbt.ivy.home=/opt/sbt-cache/ivy -Dsbt.override.build.repos=true -Dsbt.repository.config=/opt/sbt/repositories"
COPY recipe/smoke.py recipe/sources.lock.json /opt/ci-image/
WORKDIR /work
CMD ["bash"]
